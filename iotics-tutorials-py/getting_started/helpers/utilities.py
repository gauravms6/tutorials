import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from typing import Optional

from requests import Response, request


def make_api_call(
    method: str,
    endpoint: str,
    headers: Optional[dict] = None,
    payload: Optional[dict] = None,
) -> dict:
    try:
        req_resp: Response = request(
            method=method, url=endpoint, headers=headers, json=payload
        )
        req_resp.raise_for_status()
        response: dict = req_resp.json()
    except Exception as ex:
        print("Getting error", ex)
        sys.exit(1)

    return response


def print_property_rest(prop: dict, formatting=""):
    """This method will be used to print in a nice way
    the list of Properties of Twin, Feeds and Inputs."""

    property_key = prop.get("key")
    print(f"{formatting}-  Key: {property_key}")
    property_uri: dict = prop.get("uriValue")
    property_lang_literal: dict = prop.get("langLiteralValue")
    property_string_literal: dict = prop.get("stringLiteralValue")
    property_literal: dict = prop.get("literalValue")
    if property_uri:
        print(f"{formatting}   URI Value:", property_uri.get("value"))
    if property_lang_literal:
        print(f"{formatting}   Lang Literal Value:", property_lang_literal.get("value"))
        print(f"{formatting}   Lang:", property_lang_literal.get("lang"))
    if property_string_literal:
        print(
            f"{formatting}   String Literal Value:",
            property_string_literal.get("value"),
        )
    if property_literal:
        print(f"{formatting}   Literal Value:", property_literal.get("value"))
        print(f"{formatting}   Datatype:", property_literal.get("dataType"))


def print_property_grpc(prop, formatting=""):
    """This method will be used to print in a nice way
    the list of Properties of Twin, Feeds and Inputs."""

    property_key = prop.key
    print(f"{formatting}-  Key: {property_key}")
    property_uri = prop.uriValue.value
    property_lang_literal_value = prop.langLiteralValue.value
    property_lang_literal_lang = prop.langLiteralValue.lang
    property_string_literal_value = prop.stringLiteralValue.value
    property_literal_value = prop.literalValue.value
    property_literal_datatype = prop.literalValue.dataType
    if property_uri:
        print(f"{formatting}   URI Value:", property_uri)
    if property_lang_literal_value:
        print(f"{formatting}   Lang Literal Value:", property_lang_literal_value)
    if property_lang_literal_lang:
        print(f"{formatting}   Lang:", property_lang_literal_lang)
    if property_string_literal_value:
        print(f"{formatting}   String Literal Value:", property_string_literal_value)
    if property_literal_value:
        print(f"{formatting}   Literal Value:", property_literal_value)
    if property_literal_datatype:
        print(f"{formatting}   Datatype:", property_literal_datatype)


def print_value_rest(value: dict, formatting=""):
    value_label = value.get("label")
    value_comment = value.get("comment")
    value_unit = value.get("unit")
    value_datatype = value.get("dataType")

    print(f"{formatting}-  Label:", value_label)
    print(f"{formatting}   Comment:", value_comment)
    print(f"{formatting}   Unit:", value_unit)
    print(f"{formatting}   Datatype:", value_datatype)


def print_value_grpc(value: dict, formatting=""):
    value_label = value.get("label")
    value_comment = value.get("comment")
    value_unit = value.get("unit")
    value_datatype = value.get("dataType")

    print(f"{formatting}-  Label:", value_label)
    print(f"{formatting}   Comment:", value_comment)
    print(f"{formatting}   Unit:", value_unit)
    print(f"{formatting}   Datatype:", value_datatype)



def extract_twin_locations_to_csv(twins_found_list, file_path):
    data = []
    for twin in twins_found_list:
        twin_id = twin.twinId.id
        host_id = twin.twinId.hostId
        location = twin.location
        twin_properties = twin.properties

        if location:
            lat = location.lat
            lon = location.lon
        else:
            lat = None
            lon = None
        data.append({
            'Twin ID': twin_id,
            'HOST ID': host_id,
            'Latitude': lat,
            'Longitude': lon,
        })
    twins_locations = pd.DataFrame(data)
    twins_locations.to_csv(file_path, index=False)

def save_twin_properties_to_csv(twins_found_list, file_path):
    twin_ids = []
    property_keys = []
    uri_values = []
    langs = []
    lang_literal_values = []
    string_literal_values = []
    numerical_values = []
    label_name = []

    for twin in twins_found_list:
        twin_id = twin.twinId.id
        host_id = twin.twinId.hostId

        for twin_property in twin.properties:
            if twin_property.key:
                twin_ids.append(twin_id)
                property_keys.append(twin_property.key)

                if "label" in twin_property.key.lower():
                    label_name.append(twin_property.langLiteralValue.value)
                else:
                    label_name.append(None)
                
                if twin_property.uriValue and twin_property.uriValue.value:
                    uri_values.append(twin_property.uriValue.value)
                else:
                    uri_values.append(None)
                
                if twin_property.langLiteralValue and twin_property.langLiteralValue.lang and twin_property.langLiteralValue.value:
                    langs.append(twin_property.langLiteralValue.lang)
                    lang_literal_values.append(twin_property.langLiteralValue.value)
                else:
                    langs.append(None)
                    lang_literal_values.append(None)
                
                if twin_property.stringLiteralValue and twin_property.stringLiteralValue.value:
                    string_literal_values.append(twin_property.stringLiteralValue.value)
                else:
                    string_literal_values.append(None)
                
                if twin_property.literalValue and twin_property.literalValue.value and twin_property.literalValue.dataType:
                    numerical_values.append(twin_property.literalValue.value)
                else:
                    numerical_values.append(None)

    data = {
        'Twin ID': twin_ids,
        'Property Key': property_keys,
        'URI Value': uri_values,
        'Lang': langs,
        'Lang Literal Value': lang_literal_values,
        'String Literal Value': string_literal_values,
        'Numerical Values': numerical_values,
        'Label': label_name
    }

    twin_properties_df = pd.DataFrame(data)
    twin_properties_df.to_csv(file_path, index=False)

def save_twins_feeds_inputs(twins_found_list, output_csv):
    data = []
    
    for twin in twins_found_list:
        twin_id = twin.twinId.id
        host_id = twin.twinId.hostId

        for twin_feed in twin.feeds:
            feed_id = twin_feed.feedId.id
            data.append({'Twin ID': twin_id, 'Host ID': host_id, 'Feed ID': feed_id, 'Input ID': None})

        for twin_input in twin.inputs:
            input_id = twin_input.inputId.id
            data.append({'Twin ID': twin_id, 'Host ID': host_id, 'Feed ID': None, 'Input ID': input_id})

    twins_feeds_inputs = pd.DataFrame(data)
    twins_feeds_inputs.to_csv(output_csv, index=False)
    print("Data saved to", output_csv)

def Dsave_twin_properties_to_csv(twins_found_list, file_path):
    property_data = {}

    # Extract property data
    for twin in twins_found_list:
        twin_id = twin.twinId.id

        for twin_property in twin.properties:
            if twin_property.key:
                property_key = twin_property.key

                # Add property key to dictionary if not already present
                if property_key not in property_data:
                    property_data[property_key] = []

                # Append property value to corresponding property key
                if twin_property.uriValue and twin_property.uriValue.value:
                    property_data[property_key].append(twin_property.uriValue.value)
                elif twin_property.langLiteralValue and twin_property.langLiteralValue.value:
                    property_data[property_key].append(twin_property.langLiteralValue.value)
                elif twin_property.stringLiteralValue and twin_property.stringLiteralValue.value:
                    property_data[property_key].append(twin_property.stringLiteralValue.value)
                elif twin_property.literalValue and twin_property.literalValue.value:
                    property_data[property_key].append(twin_property.literalValue.value)
                else:
                    # If property value is empty, append None
                    property_data[property_key].append(None)

    # Create DataFrame from property data dictionary
    twin_properties_df = pd.DataFrame(property_data)

    # Save DataFrame to CSV
    twin_properties_df.to_csv(file_path, index=False)

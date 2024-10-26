from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from tqdm import tqdm
from vaapi.client import Vaapi
import traceback

def get_key_and_dict_by_name(dictionary1, dictionary2, name):
    #print("\tchecking the dict")
    for key, value in dictionary1.items():
        #print(f"\t{value}")
        if value['name'] == name:
            return key, dictionary1
        
    for key, value in dictionary2.items():
        #print(f"\t{value}")
        if value['name'] == name:
            return key, dictionary2
    return None, None  # Return None if name is not found

def is_behavior_done(data):
    print("\tcheck inserted behavior frames")
    try:
        # we use list here because we only know the log_id here and not the if of the logstatus object
        response = client.log_status.list(log_id=data.id)
        if len(response) == 0:
            return False
        log_status = response[0]
    except Exception as e:
        print(e)

    if not log_status.num_cognition_frames or int(log_status.num_cognition_frames) == 0:
        print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
        print(log_status.num_cognition_frames)
        return False
    
    print("\tcheck inserted behavior frames")
    if log_status.num_cognition_frames and int(log_status.num_cognition_frames) > 0:
        print(f"\tcognition frames are {log_status.num_cognition_frames}")
        response = client.xabsl_symbol_sparse.get_behavior_count(log_id=data.id)
        print(f"\tbehavior frames are {response['count']}")
        return response["count"] == int(log_status.num_cognition_frames)
    else:
        return False

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path

        print(log_path)
        # check if we need to insert this log
        if is_behavior_done(data):
            print("\tbehavior already inserted, will continue with the next log")
            continue

        my_parser = Parser()
        game_log = LogReader(str(log_path), my_parser)
        combined_symbols = list()
        
        output_decimal_lookup = dict()  # will be updated on each frame
        output_boolean_lookup = dict()  # will be updated on each frame
        output_enum_lookup = dict()
        input_decimal_lookup = dict()  # will be updated on each frame
        input_boolean_lookup = dict()  # will be updated on each frame
        broken_behavior = False

        for idx, frame in enumerate(tqdm(game_log, desc=f"Parsing frame", leave=True)):
            if 'FrameInfo' in frame:
                fi = frame['FrameInfo']
            else:
                print(f"frame {idx} does not have frame info representation so we dont go further")
                print("it could be that there is one more behavior frame in the next frame but this is one is not finished.")
                break

            if "BehaviorStateComplete" in frame:
                try:
                    full_behavior = frame["BehaviorStateComplete"]
                except Exception as e:
                    traceback.print_exc() 
                    print("can't parse the Behavior will continue with the next log")
                    broken_behavior = True
                    break
                
                """
                # TODO: idea here is to build a enumeration lookup table that we use when inserting data
                
                {
                2 : {
                    name: arm.type
                    enums: {
                        0: 'arm.type.hold'
                        1: 'arm.type.set_left_shoulder_position'
                        2: 'arm.type.set_left_shoulder_stiffness', 
                        3:'arm.type.set_left_elbow_position', 
                        4'arm.type.set_left_elbow_stiffness', 
                        5'arm.type.set_right_shoulder_position', 
                        6'arm.type.set_right_shoulder_stiffness', 
                        7'arm.type.set_right_elbow_position', 
                        8'arm.type.set_right_elbow_stiffness', 
                        9'arm.type.set_left_arm_joint_position', 
                        10'arm.type.set_left_arm_joint_stiffness', 
                        11'arm.type.set_right_arm_joint_position', 
                        12'arm.type.set_right_arm_joint_stiffness', 
                        13'arm.type.set_both_arms_joint_position', 
                        14'arm.type.set_both_arms_joint_stiffness', 
                        15'arm.type.arms_none', 
                        16'arm.type.arms_back', 
                        17'arm.type.arms_down', 
                        18'arm.type.arms_synchronised_with_walk', 
                        19 'arm.type.unknown'
                    }
                    }
                }
                """
                """
                # create a dict with all enums and their possible values
                enumeration_lookup = dict()
                for i, enum in enumerate(full_behavior.enumerations):
                    enum_dict = {}
                    for a in enum.elements:
                        enum_dict.update({a.value: a.name})
                    output = {i: {"name": enum.name, "enum": enum_dict}}
                    enumeration_lookup.update(output)
                #print(enumeration_lookup)
                
                # here we first create another lookup table, matching output id's to typeID (id's in enumeration_lookup)
                # and then we create the dict we will send to the database
                output_enumeration_lookup = dict() # needed for sparse behavior later
                output_enum_values = dict()
                for item in full_behavior.outputSymbolList.enumerated:
                    #print(item)
                    a = {item.id: {"typeId": item.typeId}}
                    print(a, item.name)
                    output_enumeration_lookup.update(a)

                    #print(enumeration_lookup[item.typeId])
                    b = {item.name: enumeration_lookup[item.typeId]["enum"][item.value]}
                    output_enum_values.update(b)

                print(output_enum_values)
                
                # here we first create another lookup table, matching inputs id's to typeID (id's in enumeration_lookup)
                # and then we create the dict we will send to the database
                input_enumeration_lookup = dict()
                input_enum_values = dict()
                for item in full_behavior.inputSymbolList.enumerated:
                    a = {item.id: {"typeId": item.typeId}}
                    print(a, item.name)
                    print(item)
                    input_enumeration_lookup.update(a)
                    b = {item.name: enumeration_lookup[item.typeId]["enum"][item.value]}
                    input_enum_values.update(b)
                print(input_enum_values)
                """
                # TODO put this in the behavior full table
                # create a lookup table for current decimal output symbols
                for i, item in enumerate(full_behavior.outputSymbolList.decimal):
                    output_decimal_lookup.update({i: {"name":item.name, "value":item.value}})

                for i, item in enumerate(full_behavior.outputSymbolList.boolean):
                    output_boolean_lookup.update({i: {"name":item.name, "value":item.value}})

                output_symbols = dict()
                for k, v in output_decimal_lookup.items():
                    output_symbols.update({v["name"]:v["value"]})

                for k, v in output_boolean_lookup.items():
                    output_symbols.update({v["name"]:v["value"]})

                # create a lookup table for current decimal input symbols
                for i, item in enumerate(full_behavior.inputSymbolList.decimal):
                    input_decimal_lookup.update({i: {"name":item.name, "value":item.value}})

                # create a lookup table for current boolean input symbols
                for i, item in enumerate(full_behavior.inputSymbolList.boolean):
                    input_boolean_lookup.update({i: {"name":item.name, "value":item.value}})

                input_symbols = dict()
                for k, v in input_decimal_lookup.items():
                    input_symbols.update({v["name"]:v["value"]})

                for k, v in input_boolean_lookup.items():
                    input_symbols.update({v["name"]:v["value"]})

                data = {
                    "input": input_symbols,
                    "output": output_symbols,
                }
                json_obj = {
                        "log_id":log_id,
                        "data": data,
                }

                try:
                    response = client.xabsl_symbol_complete.create(
                        data = json_obj
                    )
                except Exception as e:
                    print(f"error inputing the data {log_path}")
                    print(e)
                    quit()

            if "BehaviorStateSparse" in frame:
                sparse_behavior = frame["BehaviorStateSparse"]

                output_symbols = dict()
                for i, item in enumerate(sparse_behavior.outputSymbolList.decimal):
                    # get the current value for all values that changed
                    name = output_decimal_lookup[item.id]['name']
                    output_symbols.update({name:item.value})
                
                for i, item in enumerate(sparse_behavior.outputSymbolList.boolean):
                    # get the current value for all values that changed
                    name = output_boolean_lookup[item.id]['name']
                    output_symbols.update({name:item.value})

                input_symbols = dict()
                for i, item in enumerate(sparse_behavior.inputSymbolList.decimal):
                    # get the current value for all values that changed
                    name = input_decimal_lookup[item.id]['name']
                    input_symbols.update({name:item.value})

                for i, item in enumerate(sparse_behavior.inputSymbolList.boolean):
                    # get the current value for all values that changed
                    name = input_boolean_lookup[item.id]['name']
                    input_symbols.update({name:item.value})

                data = {
                    "input": input_symbols,
                    "output": output_symbols,
                }
                json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "data": data,
                }

                combined_symbols.append(json_obj)
                
                
            if idx % 25 == 0:
                try:
                    response = client.xabsl_symbol_sparse.bulk_create(
                        data = combined_symbols
                    )
                except Exception as e:
                    print(f"error inputing the data {log_path}")
                    print(e)
                    quit()
                combined_symbols.clear()


        # if we abort in BehaviorStateComplete we should not do this here
        if not broken_behavior:
            try:
                response = client.xabsl_symbol_sparse.bulk_create(
                    data=combined_symbols
                )
                #print(f"\t{response}")
            except Exception as e:
                print(f"error inputing the xabsl symbols {log_path}")
                print(e)
                quit()

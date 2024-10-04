from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from tqdm import tqdm
from vaapi.client import Vaapi
import traceback
import copy


def is_behavior_done(data):
    print("\tcheck inserted behavior frames")
    if data.num_cognition_frames and int(data.num_cognition_frames) > 0:
        print(f"\tcognition frames are {data.num_cognition_frames}")
        
        symbol_count = len(client.xabsl_symbol.list(log_id=log_id, symbol_name="game.time_in_play"))
        print(f"\tbehavior symbols are {symbol_count}")
        return symbol_count == int(data.num_cognition_frames)
    else:
        return False

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    #log_root_path = "/mnt/c/RoboCup/rc24"
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

        print(log_path, " - ", log_id)
        if not data.num_cognition_frames or int(data.num_cognition_frames) == 0:
            print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
            continue
        
        # check if we need to insert this log
        if is_behavior_done(data):
            print("\tbehavior already inserted, will continue with the next log")
            continue

        my_parser = Parser()
        game_log = LogReader(str(log_path), my_parser)
        combined_symbols = list()
        
        output_decimal_lookup = dict()  # will be updated on each frame
        output_boolean_lookup = dict()  # will be updated on each frame
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
                # TODO: idea here is to build a enumeration lookup table that we use when inserting data
                """
                enumeration_lookup_list = list()
                for i, enum in enumerate(full_behavior.enumerations):
                    elem = [a.name for a in enum.elements]
                    enum_dict = {enum.name: elem}
                    #print()
                    #print(enum)
                    #print()
                    #print(enum_dict)
                    #print()
                    #print(type(elem))
                    #print(elem)

                    #for item in enum.elements:
                    #    self.sql_queue.put(("INSERT INTO behavior_enumerations VALUES (?,?,?,?,?)", [log_num, i, enum.name, item.value, item.name]))
                    break
                """
                # create a lookup table for current decimal output symbols
                for i, item in enumerate(full_behavior.outputSymbolList.decimal):
                    output_decimal_lookup.update({i: {"name":item.name, "value":item.value}})

                #print(full_behavior.outputSymbolList.boolean)
                for i, item in enumerate(full_behavior.outputSymbolList.boolean):
                    output_boolean_lookup.update({i: {"name":item.name, "value":item.value}})
                #print()
                #print()
                #print(output_boolean_lookup)
                # create a lookup table for current decimal input symbols
                for i, item in enumerate(full_behavior.inputSymbolList.decimal):
                    input_decimal_lookup.update({i: {"name":item.name, "value":item.value}})

                # create a lookup table for current boolean input symbols
                for i, item in enumerate(full_behavior.inputSymbolList.boolean):
                    input_boolean_lookup.update({i: {"name":item.name, "value":item.value}})
            
            if "BehaviorStateSparse" in frame:
                # TODO build a check that makes sure behaviorcomplete was parsed already
                sparse_behavior = frame["BehaviorStateSparse"]

                # update the decimal output symbols
                for i, item in enumerate(sparse_behavior.outputSymbolList.decimal):
                    output_decimal_lookup[item.id]["value"]= item.value
                
                # update the boolean output symbols
                output_boolean_lookup_temp = copy.deepcopy(output_boolean_lookup)
                for i, item in enumerate(sparse_behavior.outputSymbolList.boolean):
                    output_boolean_lookup_temp[item.id]["value"]= item.value
                if fi.frameNumber == 6068:
                    print(fi.frameNumber)
                    print(output_boolean_lookup_temp)
                    print()
                if fi.frameNumber == 6069:
                    print(fi.frameNumber)
                    print(output_boolean_lookup_temp)
                    print()
                """
                if fi.frameNumber == 5781:
                    print(sparse_behavior.outputSymbolList.boolean)
                    print()
                    print(output_boolean_lookup_temp)
                if fi.frameNumber == 5782:
                    print(sparse_behavior.outputSymbolList.boolean)
                    print()
                    print(output_boolean_lookup_temp)

                if fi.frameNumber == 5783:
                    print(sparse_behavior.outputSymbolList.boolean)
                    print()
                    print(output_boolean_lookup_temp)
                    quit()
                """

                # update the decimal input symbols
                for i, item in enumerate(sparse_behavior.inputSymbolList.decimal):
                    input_decimal_lookup[item.id]["value"]= item.value

                # update the boolean input symbols
                input_boolean_lookup_temp = copy.deepcopy(input_boolean_lookup)
                for i, item in enumerate(sparse_behavior.inputSymbolList.boolean):
                    input_boolean_lookup_temp[item.id]["value"]= item.value
                
                """
                for k, v in output_boolean_lookup.items():
                    if v["name"] == "arm.react_to_collision":
                        if found_first:
                            print(fi.frameNumber, found_first)
                        if v["value"] == last_value:
                            pass
                        else:
                            print(fi.frameNumber)
                            print(v)
                            last_value = v["value"]
                            found_first = True
                """
                for k, v in output_decimal_lookup.items():
                    #output_decimal.update({v["name"]:v["value"]})
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "output_decimal",
                        "symbol_name":v["name"],
                        "symbol_value":str(v["value"]),
                    }
                    combined_symbols.append(json_obj)

                for k, v in output_boolean_lookup_temp.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "output_boolean",
                        "symbol_name":v["name"],
                        "symbol_value":str(v["value"]),
                    }
                    combined_symbols.append(json_obj)

                for k, v in input_decimal_lookup.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "input_decimal",
                        "symbol_name":v["name"],
                        "symbol_value":v["value"],
                    }
                    combined_symbols.append(json_obj)

                for k, v in input_boolean_lookup_temp.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "input_boolean",
                        "symbol_name":v["name"],
                        "symbol_value":str(v["value"]),
                    }
                    combined_symbols.append(json_obj)

                
            if idx % 15 == 0:
                try:
                    response = client.xabsl_symbol.bulk_create(
                        data_list = combined_symbols
                    )
                except Exception as e:
                    print(f"error inputing the data {log_path}")
                    print(e)
                    quit()
                combined_symbols.clear()


        # if we abort in BehaviorStateComplete we should not do this here
        if not broken_behavior:
            try:
                response = client.xabsl_symbol.bulk_create(
                    data_list=combined_symbols
                    )
            except Exception as e:
                print(f"error inputing the xabsl symbols {log_path}")
                print(e)

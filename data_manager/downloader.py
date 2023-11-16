import subprocess
import time


app_path = "C:/app/tools/IBM/DOORS/9.6_64/bin/doors.exe"
database_path = "36677@skobde-doors9db.ad.trw.com"
user_name = "SynekO"
user_passwd = "gt1400Frk+"
dxl_file = "doors_downloader.dxl"

doors_cmd = fr'{app_path} -data "{database_path}" -u "{user_name}" -P "{user_passwd}" -batch "{dxl_file}"'

# time_start = time.time()

# subprocess.call(doors_cmd, shell=False)

# time_end = time.time()

# time_delta = time_end - time_start

# print(f'Downloading took {time_delta} seconds')




def _create_dxl_columns_string(module_columns: list) -> str:
    return ''.join(['"<<<COLUMN>>>"o."' + column + '"' for column in module_columns])



def _create_dxl_query(
    module_path: str,
    module_columns: list[str],):
    dxl_query = r'''
    
    m = read("''' + str(module_path) + r'''",true)
    module_name = name m
    module_path = path m
    out << "<<<MODULE>>><<<PATH>>>" module_path "/" module_name ""

    for o in entire(m) do {
        out << "<<<REQUIREMENT>>><<<ID>>>"identifier(o)"<<<LEVEL>>>"level(o)"<<<HEADING>>>"o."Object Heading"''' + _create_dxl_columns_string(module_columns) + r'''""
        for outLink in (o -> "*") do {
            out << "<<<OUTLINK>>>"(fullName targetVersion outLink) ":" (targetAbsNo (outLink)) "" 
        }
    }

    '''
    return dxl_query



def _create_dxl_script(module_paths:list[str], module_columns:list[list]):
    dxl_header = r"""
    // Turn off runlimit for timing
    pragma encoding,"utf-8"
    pragma runLim,0

    string file_location = "data/doors_output.txt"

    // Open stream
    Stream out = write file_location
    Object o
    Link outLink
    Module m
    string module_name 
    """

    content = ""

    for i in range(len(module_paths)):
        content += _create_dxl_query(module_paths[i], module_columns[i])
        content += "\n"



    return dxl_header + content


def create_and_run_dxl_script(
    module_paths: list[str],
    module_columns: list[list[str]],):





    file_content = _create_dxl_script(module_paths, module_columns)
    # print(file_content)

    with open(dxl_file, 'w', encoding='utf8') as new_dxl_file:
        new_dxl_file.write(file_content)
        
    subprocess.call(doors_cmd, shell=False)    





    




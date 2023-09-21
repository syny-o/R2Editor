def reduce_path_string(path):
    # path_length = len(path)
    # if path_length > 70:
    #     difference = path_length - 70
    #     reduced_path = f"...{path[difference:]}"
    #     return reduced_path
    # return path

    path = path.replace("\\", "/")
    path_list = path.split("/")
    # print(path_list)
    if len(path_list) > 1:
        return "/".join(path_list[-2:])
    else:
        return "/".join(path_list)
    
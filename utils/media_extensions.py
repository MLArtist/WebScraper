import mimetypes

import config


def get_extensions_for_type():
    return_list = set()
    general_type = config.EXCLUDED_URL_EXTENSIONS
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] in general_type:
            return_list.add(ext.lower())
    return return_list

media_extensions_list = get_extensions_for_type()
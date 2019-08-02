import json

def writeToConfig(use_parse_tree,
            use_dependencies,
            dependecy_level,
            use_dependencies_with_coref,
            use_existing_hearst,
            hearst_patterns,
            hearst_pattern_type,
            language,
            addn,
            use_spotlight):
    """
    Write to config json, which is saved and then read to apply required configuration
    """
    configdata = {
        "use_parse_tree": use_parse_tree,
        "use_dependencies": use_dependencies,
        "dependency_level": dependecy_level,
        "use_dependencies_with_coref": use_dependencies_with_coref,
        "use_existing_hearst": use_existing_hearst,
        "addn_hearst_patterns": hearst_patterns,
        "hearst_pattern_type": hearst_pattern_type,
        "language": language,
        "addn": addn,
        "use_spotlight": use_spotlight
    }

    with open('config.json', 'w') as f:
        json.dump(configdata, f)

def readFromConfig():
    with open('config.json') as f:
        configdata = json.load(f)
    return configdata
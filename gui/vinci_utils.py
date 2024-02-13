import collections

# ---------------------------- PRESETS ARE DEFINED HERE ----------------------------

CODE_DX_PRESET_XML_ROOT = "report->findings->finding"
GENDARME_PRESET_XML_ROOT = "gendarme-output->results->rule"
SPOTBUGS_PRESET_XML_ROOT = "BugCollection->BugInstance"
FORTIFY_PRESET_XML_ROOT = "FVDL->Vulnerabilities->Vulnerability"
CPPCHECK_PRESET_XML_ROOT = "results->errors->error"
PMD_PRESET_ROOT = "pmd->file->violation"
JSHINT_PRESET_ROOT = "checkstyle->file->error" # cannot get the file name, need to do more tests
PHP_CODESNIFFER_PRESET_ROOT = "phpcs->file->error"
#PYLINT_PRESET_ROOT= 

CODE_DX_PRESET_XML = [
    "@status",
    "@severity",
    "cwe->@id",
    "results->result->description->#text",
    "results->result->tool->@category",
    "results->result->tool->@name",
    "rule->@code",
    "rule->@name",
]

CODE_DX_PRESET_CSV = [
    "@status",
    "@severity",
    "cwe->@id",
    "results->result->description->#text",
    "results->result->tool->@category",
    "results->result->tool->@name",
    "rule->@code",
    "rule->@name",]

PMD_PRESET_CSV = [
    "Status",
    "Problem",
    "Package",
    "File",
    "Priority",
    "Line",
    "Description",
    "Rule set",
    "Rule",]

PMD_PRESET_XML = [
    "@status",
    "@beginline",
    "@endline",
    "@begincolumn",
    "@endcolumn",
    "@rule",
    "@ruleset",
    "@externalInfoUrl",
    "@priority",
    # "@description",
]

PMD_PRESET_JSON = [
    "beginline",
    "begincolumn",
    "endline",
    "endcolumn",
    "description",
    "rule",
    "ruleset",
    "priority",
    "externalInfoUrl"]

PHP_CODESNIFFER_PRESET_XML = [
    "@status",
    "@file",
    "@line",
    "@column",
    "@source",
    "@severity",
    "@fixable",
]

PHP_CODESNIFFER_PRESET_CSV = [
    "Status",
    "File",
    "Line",
    "Column",
    "Type",
    "Message",
    "Source",
    "Severity",
    "Fixable",
]

PHP_CODESNIFFER_PRESET_JSON = [
    "message",
    "source",
    "severity",
    "fixable",
    "type",
    "line",
    "column"
]

GENDARME_PRESET_XML = [
    "output",
    "@Name",
    "target->defect->@Severity",
    "target->defect->@Confidence",
]

SPOTBUGS_PRESET_XML = [
    "output",
    "@type",
    "@priority",
    "@rank",
    "@category",
    "Class->SourceLine->@sourcefile",
]

FORTIFY_PRESET_XML = [
    "output",
    "ClassInfo->Kingdom",
    "ClassInfo->Type",
    "ClassInfo->Subtype",
    "ClassInfo->AnalyzerName",
    "ClassInfo->DefaultSeverity",
    "InstanceInfo->InstanceSeverity",
    "InstanceInfo->Confidence",
]

CPPCHECK_PRESET_XML = [
    "output",
    "@id",
    "@severity",
    "@msg",
]

PYLINT_PRESET_JSON = [
    "type",
    "module",
    "obj",
    "line",
    "column",
    "endLine",
    "endColumn",
    "path",
    "symbol",
    "message",
    "message-id"
]

JSHINT_PRESET_JSON = [
    "raw",
    "evidence",
    "line",
    "character",
    "scope",
    "reason"
]

JSHINT_PRESET_XML = [
    "output",
    "@line",
    "@column",
    "@severity",
    "@message"
]

ESLINT_PRESET_JSON = [
 
    "ruleId",
    "severity",
    "message",
    "line",
    "column",
    "nodeType",
    "messageId"
]

# ---------------------------- PRESETS END HERE ----------------------------

# ---------------------------- CWSS DATA --------------------------------------

CWSS_DATA = {
    "base_finding": {
        "ti": {
            "selections": [
                "Critical",
                "High",
                "Medium",
                "Low",
                "None",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["C", "H", "M", "L", "N", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.6, 0.3, 0.0, 0.6, 0.5, 1.0],
        },
        "ap": {
            "selections": [
                "Administrator",
                "Partially-Privileged User",
                "Regular User",
                "Limited/Guest",
                "None",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["A", "P", "RU", "L", "N", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.7, 0.6, 0.1, 0.7, 0.5, 1.0],
        },
        "al": {
            "selections": [
                "Application",
                "System",
                "Network",
                "Enterprise Infrastructure",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["A", "S", "N", "E", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.7, 1.0, 0.9, 0.5, 1.0],
        },
        "ic": {
            "selections": [
                "None",
                "Limited",
                "Moderate",
                "Indirect (Defense-in-Depth)",
                "Best-Available",
                "Complete",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["N", "L", "M", "I", "B", "C", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.7, 0.5, 0.3, 0.0, 0.6, 0.5, 1.0],
        },
        "fc": {
            "selections": [
                "Proven True",
                "Proven Locally True",
                "Proven False",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["L", "LT", "F", "D", "UK", "NA"],
            "values": [1.0, 0.8, 0.0, 0.8, 0.5, 1.0],
        },
    },
    "attack_surface": {
        "rp": {
            "selections": [
                "None",
                "Limited/Guest",
                "Regular User",
                "Partially-Privileged User",
                "Administrator",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["N", "L", "RU", "P", "A", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.7, 0.6, 0.1, 0.7, 0.5, 1.0],
        },
        "rl": {
            "selections": [
                "Application",
                "System",
                "Network",
                "Enterprise Infrastructure",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["A", "S", "N", "E", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.7, 1.0, 0.9, 0.5, 1.0],
        },
        "av": {
            "selections": [
                "Internet",
                "Intranet",
                "Private Network",
                "Adjacent Network",
                "Local",
                "Physical",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["I", "R", "V", "A", "L", "P", "D", "U", "NA"],
            "values": [1.0, 0.8, 0.8, 0.7, 0.5, 0.2, 0.75, 0.5, 1.0],
        },
        "as": {
            "selections": [
                "Strong",
                "Moderate",
                "Weak",
                "None",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["S", "M", "W", "N", "D", "UK", "NA"],
            "values": [0.7, 0.8, 0.9, 1.0, 0.85, 0.5, 1.0],
        },
        "in": {
            "selections": [
                "Automated",
                "Typical/Limited",
                "Moderate",
                "Opportunistic",
                "High",
                "No Interaction",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["A", "T", "M", "O", "H", "NI", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.8, 0.3, 0.1, 0.0, 0.55, 0.5, 1.0],
        },
        "sc": {
            "selections": [
                "All",
                "Moderate",
                "Rare",
                "Potentially Reachable",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["A", "M", "R", "P", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.5, 0.1, 0.7, 0.5, 1.0],
        },
    },
    "environmental": {
        "bi": {
            "selections": [
                "Critical",
                "High",
                "Medium",
                "Low",
                "None",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["C", "H", "M", "L", "N", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.6, 0.3, 0.0, 0.6, 0.5, 1.0],
        },
        "di": {
            "selections": [
                "High",
                "Medium",
                "Low",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["H", "M", "L", "D", "UK", "NA"],
            "values": [1.0, 0.6, 0.2, 0.6, 0.5, 1.0],
        },
        "ex": {
            "selections": [
                "High",
                "Medium",
                "Low",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["H", "M", "L", "D", "UK", "NA"],
            "values": [1.0, 0.6, 0.2, 0.6, 0.5, 1.0],
        },
        "ec": {
            "selections": [
                "None",
                "Limited",
                "Moderate",
                "Indirect (Defense-in-Depth)",
                "Best-Available",
                "Complete",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["N", "L", "M", "I", "B", "C", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.7, 0.5, 0.3, 0.1, 0.6, 0.5, 1.0],
        },
        "p": {
            "selections": [
                "Widespread",
                "High",
                "Common",
                "Limited",
                "Default",
                "Unknown",
                "Not Applicable",
            ],
            "letters": ["W", "H", "C", "L", "D", "UK", "NA"],
            "values": [1.0, 0.9, 0.8, 0.7, 0.85, 0.5, 1.0],
        },
    },
}

# ---------------------------- CWSS DATA ENDS HERE ----------------------------


def findRoots(d, curr_root=[], possibleRoots=[]):
    """Finds roots in a dictionary.
    A root is a list object inside a dictionary.
    Such list object is found by searching recursively in the dictionary.

    Args:
        d (dict): Dictionary to search on.
        curr_root (list, optional): Current depth level in dictionary. Defaults to [].
        possibleRoots (list, optional): Roots found so far. Defaults to [].

    Returns:
        list: List of possible roots.
    """
    if type(d) == dict:
        for k in d.keys():
            curr_root.append(k)
            if type(d[k]) == list:
                possibleRoots.append(curr_root.copy())
            findRoots(d[k], curr_root, possibleRoots)
            curr_root.remove(k)
    return possibleRoots


def findColumns(d, curr_col=[], possibleCols=[]):
    """Finds possible columns in a dictionary.
    Dictionary is searched recursively.
    A column is a string object.

    Args:
        d (dict): Dictionary to search on.
        curr_col (list, optional): Current depth level inside dictionary. Defaults to [].
        possibleCols (list, optional): Columns found so far. Defaults to [].

    Returns:
        list: List of possible columns.
    """
    if type(d) == dict:
        for k in d.keys():
            curr_col.append(k)
            if type(d[k]) == str:
                possibleCols.append(curr_col.copy())
            findColumns(d[k], curr_col, possibleCols)
            curr_col.remove(k)
    return possibleCols

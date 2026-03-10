import re


def extract_params(code: str):
    """
    Extract all PARAM variables from code.
    Returns dict: {name: {value, min, max, type}}

    Supports multiple formats:
        module = 2         # PARAM (1, 5)
        num_teeth = 20     # PARAM (10, 100)
        helix_angle = 15.5 # PARAM (5.0, 45.0)
    """
    # More robust pattern that handles whitespace variations and optional decimals
    pattern = r"(\w+)\s*=\s*([\d\.]+)\s*#\s*PARAM\s*\(\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\)"
    matches = re.findall(pattern, code)

    params = {}
    for name, val_str, min_str, max_str in matches:
        # Determine type based on presence of decimal point in any of the values
        is_int = all("." not in s for s in [val_str, min_str, max_str])

        try:
            val = int(val_str) if is_int else float(val_str)
            min_val = int(min_str) if is_int else float(min_str)
            max_val = int(max_str) if is_int else float(max_str)

            # Validate ranges
            if min_val > max_val:
                continue  # Skip invalid ranges
            if not (min_val <= val <= max_val):
                continue  # Skip if value is outside range

            params[name] = {
                "value": val,
                "min": min_val,
                "max": max_val,
                "type": "int" if is_int else "float"
            }
        except ValueError:
            continue  # Skip if conversion fails

    return params


def update_code_with_params(code: str, new_values: dict):
    """
    Update parameter values in code while preserving PARAM comments.
    
    Args:
        code: Original code with PARAM comments
        new_values: Dict of {var_name: new_value}
    
    Returns:
        Updated code
    """
    lines = code.split('\n')
    new_lines = []
    
    for line in lines:
        if "PARAM" in line and "#" in line:
            match = re.match(r"\s*(\w+)\s*=", line)
            if match:
                var_name = match.group(1)
                if var_name in new_values:
                    # Extract everything after #
                    comment_part = line.split("#", 1)[1]
                    new_lines.append(f"{var_name} = {new_values[var_name]} #{comment_part}")
                    continue
        
        new_lines.append(line)
    
    return "\n".join(new_lines)
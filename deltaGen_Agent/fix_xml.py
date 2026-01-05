with open('sample.drawio', 'r') as f:
    lines = f.readlines()

# Find and fix the untar cell
fixed_lines = []
for i, line in enumerate(lines):
    fixed_lines.append(line)
    if 'id="untar"' in line and i + 1 < len(lines):
        # Check if next line has geometry
        if 'mxGeometry' in lines[i + 1]:
            # Check if there's a closing tag after geometry
            if i + 2 < len(lines) and '</mxCell>' not in lines[i + 2]:
                # Add the closing tag after geometry line
                fixed_lines.append('        </mxCell>\n')
                fixed_lines.append('       \n')

with open('sample.drawio', 'w') as f:
    f.writelines(fixed_lines)

print("Fixed XML structure")

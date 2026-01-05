with open('sample.drawio', 'r') as f:
    lines = f.readlines()

# Insert the Get User Input cell after line 17 (index 17 in 0-based)
insert_lines = [
    '        <!-- Get User Input -->\n',
    '        <mxCell id="input" value="Get User Input" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">\n',
    '          <mxGeometry x="300" y="170" width="160" height="50" as="geometry"/>\n',
    '        </mxCell>\n',
    '       \n'
]

new_lines = lines[:17] + insert_lines + lines[17:]

with open('sample.drawio', 'w') as f:
    f.writelines(new_lines)

print("Added Get User Input cell")

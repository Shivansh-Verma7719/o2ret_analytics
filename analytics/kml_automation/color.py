import pandas as pd

def create_kml_styles():
    excel_file = 'colorsforkml.xlsx'

    df = pd.read_excel(excel_file, sheet_name=0, usecols='A', header=None)

    if len(df) < 98:
        raise ValueError("The Excel file must contain at least 98 rows in column A.")
    style_string = ''
    for i in range(99):
        color_value = df.iloc[i, 0]
        style_snippet = f'''
        <StyleMap id="color{i+1}">
		<Pair>
			<key>normal</key>
			<styleUrl>#color{i+1}</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#color{i+1}</styleUrl>
		</Pair>
	    </StyleMap>
        <Style id="color{i+1}">
            <PolyStyle>
                <color>ff{color_value}<color>
                <fill>1</fill>
                <outline>1</outline>
            </PolyStyle>
            <LineStyle>
                <color>ff0000ff</color>
            </LineStyle>
        </Style>\n
        '''
        style_string += style_snippet

    return style_string
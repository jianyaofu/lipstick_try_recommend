# -*- coding: utf-8 -*-

from colorsys import rgb_to_hsv
import pandas as pd
import re 

def min_color_diff(color_to_match: tuple) -> list:
    close_color ={}
    l=[]
    """ returns the `(distance, color_name)` with the minimal distance to `colors` choose 5 closest color"""
    
    #clean data
    color_df = pd.read_csv('lipstick.csv')
    color_df = color_df.drop(['Unnamed: 0'],axis = 1)
    color_df = color_df.fillna(value=str(0))
    
    #change the rgb column to tuple
    pattern = r'(\d+)'
    def get_tuple(row):
        match = re.findall(pattern, row)
        tuple_=(float(match[0]), float(match[1]), float(match[2]))
        return tuple_
    color_df['rgb'] = color_df['rgb'].apply(get_tuple)
    
    #remove 'out of stock'
    pattern_ = r'^\w{3} \w{2} \w{5}: '
    def remove_nostock(row):
        match = re.search(pattern_, row)
        if match:
            row = row[14:]
        return row
    color_df['color'] = color_df['color'].apply(remove_nostock)

    def to_hsv( color ): 
        """ converts color tuples to floats and then to hsv """
        return rgb_to_hsv(*[x/255.0 for x in color]) #rgb_to_hsv wants floats!
    color_df['hsv'] = color_df['rgb'].apply(to_hsv)

    def color_dist( c1, c2):
        """ returns the squared euklidian distance between two color vectors in hsv space """
        return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

    for i in range(len(color_df['hsv'])):
        close_color[color_df['hsv'][i]] = (color_df['brand_name'][i], color_df['product_name'][i], color_df['color'][i], color_dist(color_to_match, color_df['hsv'][i]))

    
    close_color_ = sorted(close_color.items(), key=lambda x: x[1][3])

    for key, value in close_color_:
        l.append([value[0], value[1], value[2]])
    return l[:5]
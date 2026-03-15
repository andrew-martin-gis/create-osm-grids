import math
import osmium as o
import shapely
import sys
import os

site_num = int(input("Enter the site number: "))

def create_osm_data(site_num, bldg_num, current_floor, cell_top_left, cell_bottom_right, center_node):
    # Create the OSM file for the bounding box
    with open(f"{site_num}-{bldg_num[row]}-{current_floor}.osm", "w") as f:
        f.write(f"<osm version='0.6' generator='osmium'>\n")
        f.write(f"  <bounds minlat='{cell_top_left[0]}' minlon='{cell_top_left[1]}' maxlat='{cell_bottom_right[0]}' maxlon='{cell_bottom_right[1]}'/>\n")
        f.write(f"  <node id='2' visible='true' version='1' changeset='1' lat='{float(cell_bottom_right[0])}' lon='{float(cell_bottom_right[1])}'/>\n")
        f.write(f"  <node id='3' visible='true' version='1' changeset='1' lat='{float(cell_bottom_right[0])}' lon='{float(cell_top_left[1])}'/>\n")
        f.write(f"  <node id='4' visible='true' version='1' changeset='1' lat='{float(cell_top_left[0])}' lon='{float(cell_top_left[1])}'/>\n")
        f.write(f"  <node id='5' visible='true' version='1' changeset='1' lat='{float(cell_top_left[0])}' lon='{float(cell_bottom_right[1])}'/>\n")
        f.write(f"  <node id='1' visible='true' version='1' changeset='1' lat='{float(center_node[0])}' lon='{float(center_node[1])}'>")
        f.write(f"      <tag k='name' v='origin'/>")
        f.write(f"      <tag k='site_id' v='{site_num}'/>")
        f.write(f"      <tag k='building_id' v='{bldg_num[row]}'/>")
        f.write(f"      <tag k='floor_id' v='{current_floor}'/>")
        f.write(f"  </node>")
        f.write(f"  <way id='10' visible='true' version='1' changeset='1'>")
        f.write(f"      <nd ref='2'/>")
        f.write(f"      <nd ref='3'/>")
        f.write(f"      <nd ref='4'/>")
        f.write(f"      <nd ref='5'/>")
        f.write(f"      <nd ref='2'/>")
        f.write(f"  </way>")
        f.write(f"</osm>")

def portal_coords(site_num, bldg_num, current_floor, cell_top_left, cell_bottom_right):
    # Extract the minlat, minlon, maxlat, and maxlon attributes of the bounds
    minlat = cell_top_left[0]
    minlon = cell_top_left[1]
    maxlat = cell_bottom_right[0]
    maxlon = cell_bottom_right[1]

    #Convert to bounds to Portal coordinates
    conv_c1 = format(float(minlon), ".7f")
    conv_c2 = format(float(minlat), ".7f")
    conv_c3 = format(float(maxlon), ".7f")
    conv_c4 = format(float(maxlat), ".7f")
    
    portal_coord = f"{conv_c1},{conv_c2},{conv_c3},{conv_c4}"
    print(f"{site_num}-{bldg_num[row]}-{current_floor}: {portal_coord}")

# Prompt user for input of bounding box and grid dimensions
bbox_top_left = input("Enter top left coordinate of bounding box (format: lat,lon): ")
bbox_bottom_right = input("Enter bottom right coordinate of bounding box (format: lat,lon): ")
print("Note: Campus map is automatically generated. Don't include campus map in number of buildings or any building info.")
num_bldgs = int(input("Enter number of buildings: "))
num_rows = num_bldgs + 1

# Calculate bounding box dimensions
bbox_top_left = [float(x) for x in bbox_top_left.split(",")]
bbox_bottom_right = [float(x) for x in bbox_bottom_right.split(",")]
bbox_width = bbox_bottom_right[1] - bbox_top_left[1]
bbox_height = bbox_top_left[0] - bbox_bottom_right[0]

# Prompt user for input of number of columns in each row
num_cols = []
bldg_num = []
initial_floor = []
for row in range(num_rows):
    if row == 0:
        bldg_num.append(int(0))
        num_cols.append(int(1))
        initial_floor.append(int(0))
    
    else:
        bldg_num.append(int(input(f"Row {row} - Enter the building number: ")))
        num_cols.append(int(input(f"Row {row} - Enter number of floors: ")))
        initial_floor.append(int(input(f"Row {row} - Enter the number of the initial floor: ")))

# Download OSM data for each grid cell and save to separate files
for row in range(num_rows):
    for col in range(num_cols[row]):

        fl_col = col + 1

        cell_top_left = (bbox_top_left[0] - (row * bbox_height), bbox_top_left[1] + (fl_col * bbox_width))
        cell_bottom_right = (cell_top_left[0] - bbox_height, cell_top_left[1] + bbox_width)

        center_node = (cell_top_left[0] - (bbox_height / 2), cell_top_left[1] + (bbox_width / 2))

        current_floor = initial_floor[row] + col

        create_osm_data(site_num, bldg_num, current_floor, cell_top_left, cell_bottom_right, center_node)

        portal_coords(site_num, bldg_num, current_floor, cell_top_left, cell_bottom_right)
# To run this program execute following on command prompt
# Syntax:
#   python family_tree.py <name of csv> <Graph Title>
# Example:
#   python family_tree.py homer_family_tree.csv "Simpson's Family"

import os.path
import sys
import glob, os
import pydot
from PIL import Image
import pandas as pd
from graphviz import Source
import datetime
import subprocess

if len(sys.argv) > 1:
    file_name = sys.argv[1].split(".")[0]
else:
    file_name = 'homer_family_tree'

if len(sys.argv) > 2:
    graph_label = sys.argv[2]
else:
    graph_label = "Simpson's Family"

df = pd.read_csv(file_name+".csv",index_col=False)
df.fillna('', inplace=True)
# df.sort_values(by='dob', ascending=True,inplace=True)
today = datetime.datetime.now().strftime("%d-%B-%Y %H:%M:%S")
graph = pydot.Dot(label= graph_label,
                  labelloc="t", # t: Place the graph's title on top.
                  labeljust="c",
                  fontname="Comic Sans MS",
                  fontsize  = 100, #  Make title stand out by giving a large font size
                  fontcolor = "Black",
                  graph_type='graph',
                  overlap = "compress",
                  rankdir="BT",
                #   splines='polyline',
                #   imagescale="height",
                  strict=True,
                  ranksep=0.1,
                  nodesep=0.1,
                  newrank=True,
                  concentrate=True)

# Function to remove chars other than [a-z][A-Z][0-9]
def removespaces(string):
    # print("removespaces", string)
    result = "".join(c.lower() for c in string if c.isalnum())
    return result

# Function to get the photo for the node, add missing photo where no image available
def getphoto(name):
    # print("Get Photo for :",name)
    if os.path.isfile("images/"+removespaces(name)+".thumbnail.png"):
        photograph="images/"+removespaces(name)+".thumbnail.png"
    else:
        photograph="images/missing.thumbnail.png"
    return photograph

# Function to add member node and format its label
def add_family_node(name):
    person = (df.loc[df['name'] == name].reset_index()).to_dict('list')
    if (len(person['name']) > 0):
        if not graph.get_node(person['name'][0]):
            node = pydot.Node(person['name'][0],style="invisible")
            label_text = "<<TABLE border='0' cellborder='0' cellspacing='0'>"
            label_text += "<TR><TD BORDER=\"0\"><IMG SCALE=\"TRUE\" SRC=\"" + getphoto(person['name'][0]) + "\"/></TD></TR>"    
            if person['dod'][0]:
                label_text += "<TR><TD align='center'><font color='#fa912f' POINT-SIZE='30'> &#x950; </font> </TD></TR>" #
            label_text += "<TR><TD align='center'>" + person['name'][0] + "</TD></TR>"
            if person['alias'][0]:
                label_text += "<TR><TD align='center'>a.k.a. : " + person['alias'][0] + "</TD></TR>"
            if person['dob'][0]:
                label_text += "<TR><TD align='center'>Born : " + person['dob'][0] + "</TD></TR>"
            if person['dom'][0]:
                label_text += "<TR><TD align='center'>Marriage : " + person['dom'][0] + "</TD></TR>"
            label_text += "</TABLE>>"
            node.set_label(label_text)
        else:
            node = pydot.Node(name)
    else:
        node = pydot.Node(name)
    return node

# Function to add the cluster for married couple
def add_family_cluster(person):
    if person['gender'] == 'F':
        connectionNode = removespaces(person['name']) + "_family"
    else:
        connectionNode = removespaces(person['spouse_name']) + "_family"

    if not graph.get_subgraph("cluster_"+connectionNode):
        subgraph = pydot.Cluster(connectionNode,
                                label="",
                                strict=True,
                                rank="same",
                                margin=0,
                                penwidth=0,
                                style="rounded",
                                bgcolor= "white")
        subgraph.add_node(add_family_node(person['name']))
        subgraph.add_node(pydot.Node(connectionNode,
                                    shape="circle",
                                    penwidth=0,
                                    fontsize="30pt",
                                    label="&#x26AD;",
                                    fontcolor="black",
                                    fillcolor="white",
                                    style='filled'))
        subgraph.add_node(add_family_node(person['spouse_name']))
        subgraph.add_edge(pydot.Edge(person['spouse_name'],connectionNode,constraint=False))
        subgraph.add_edge(pydot.Edge(person['name'], connectionNode,constraint=False))
        graph.add_subgraph(subgraph)
    return

# Function to iterate records and generate family tree
def generate_family_tree():
    for index, person in df.iterrows():
        if person['spouse_name']:
            add_family_cluster(person)
        else:
            graph.add_node(add_family_node(person['name']))
    for index, person in df.iterrows():
        if person['mother_name']:
            connectionNode = person['mother_name'] 
            if person['father_name']:
                connectionNode = removespaces(connectionNode) + "_family"
            edge = pydot.Edge(connectionNode,
                              person['name'],
                              penwidth=1,
                              color='red',
                              arrowhead="box", 
                              dir="forward",
                              concentrate=True,
                              style="solid")
            graph.add_edge(edge)
    return None

def generate_thumbnails():
    size = 300, 300
    # Remove old thumbnails
    for infile in glob.glob("images/*.thumbnail.png"):
        os.remove(infile)
    # Create new thumbnails
    for infile in glob.glob("images/*.*"):
        file, ext = os.path.splitext(infile)
        with Image.open(infile) as im:
            im.thumbnail(size)
            # print(file)
            im.save(file + ".thumbnail.png", "PNG")
    # Add drop-shadow to thumbnail
        cmd = "convert " + file + ".thumbnail.png" + " \( +clone -background black -shadow 80x20+0+15 \) +swap -background transparent -layers merge +repage " + file + ".thumbnail.png"
        subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    # Generate thumbnails for the pictures
    # use of thumnails protect the original pictures 
    generate_thumbnails()
    
    # Generate Family tree Graph
    generate_family_tree()
    
    # Save Graph as .dot file
    graph.write(file_name+".dot")
    
    # Read the .dot file and view, this step also generates the PDF
    s = Source.from_file(file_name+".dot")
    s.view()
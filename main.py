from typing import List
import csv
import time
import streamlit as st
import pandas as pd


# Node class with each object containing nitrogen levels, year and month, and site ID
class Node:
    def __init__(self):
        self.nitrogen = 0.0
        self.year_month = 0
        self.siteID = ""


# merge does merge sort and takes in a list of Nodes (nodes) and three integers (start, middle, end)
def merge(nodes: List[Node], start: int, middle: int, end: int):
    # splits nodes list into two
    n1 = middle - start + 1
    n2 = end - middle

    # makes two new lists (X and Y) with first and second half of nodes list
    X = nodes[start:start + n1]
    Y = nodes[middle + 1:middle + 1 + n2]

    i = 0
    j = 0
    k = start

    while i < n1 and j < n2:
        # picks the smaller of the two values (X[i] or Y[j]) to be nodes[k]
        if X[i].nitrogen <= Y[j].nitrogen:
            nodes[k] = X[i]
            i += 1
        else:
            nodes[k] = Y[j]
            j += 1
        k += 1

    # if j > n2 but i isn't > n1
    while i < n1:
        nodes[k] = X[i]
        i += 1
        k += 1

    # if i > n1 but j isn't > n2
    while j < n2:
        nodes[k] = Y[j]
        j += 1
        k += 1


# same as merge but compares year_month values for each Node object instead
def merge_by_year_month(nodes: List[Node], start: int, middle: int, end: int):
    n1 = middle - start + 1
    n2 = end - middle

    X = nodes[start:start + n1]
    Y = nodes[middle + 1:middle + 1 + n2]

    i = j = 0
    k = start

    while i < n1 and j < n2:
        if X[i].year_month <= Y[j].year_month:
            nodes[k] = X[i]
            i += 1
        else:
            nodes[k] = Y[j]
            j += 1
        k += 1

    while i < n1:
        nodes[k] = X[i]
        i += 1
        k += 1

    while j < n2:
        nodes[k] = Y[j]
        j += 1
        k += 1


def merge_sort(nodes: List[Node], start: int, end: int, sort_by: str):
    # divides nodes into half if list is greater than one
    if start < end:
        middle = start + (end - start) // 2
        merge_sort(nodes, start, middle, sort_by)
        merge_sort(nodes, middle + 1, end, sort_by)

        # sorts by year and month
        if sort_by == "year":
            merge_by_year_month(nodes, start, middle, end)
        else:
            merge(nodes, start, middle, end)


##https://stackoverflow.com/questions/33339851/how-is-the-knuth-sequence-properly-implemented-for-a-shellsort-in-java
def shell_sort(nodes: List[Node], n: int):
    # Generate the gap sequence using Knuth's formula
    gap = 1
    # Knuth's formula is shown here
    while gap <= n // 3:
        gap = gap * 3 + 1

    while gap > 0:
        for i in range(gap, n):
            temp = nodes[i]
            j = i
            # this is where the nodes on the other side of the gap
            # and the temp node are compared
            while j >= gap and nodes[j - gap].nitrogen > temp.nitrogen:
                # If the current node's nitrogen value is greater than the                temp node,
                # then the nodes are swapped which is shown here
                nodes[j] = nodes[j - gap]
                j -= gap
        nodes[j] = temp
    gap //= 3


def shell_sort_by_year_month(nodes: List[Node], n: int):
    # Generate the gap sequence using Knuth's formula
    gap = 1
    while gap <= n // 3:
        gap = gap * 3 + 1
    # Knuth's formula is shown here
    while gap > 0:
        for i in range(gap, n):
            temp = nodes[i]
            j = i
            # this is where the nodes on the other side of the gap
            # and the temp node are compared based on year/month
            while j >= gap and nodes[j - gap].year_month > temp.year_month:
                # If the current node's year and month value is greater                   than the temp node,
                # then the nodes are swapped which is shown here
                nodes[j] = nodes[j - gap]
                j -= gap
            nodes[j] = temp
        gap //= 3


# here is where the data is read in and nodes are created then inserted
def read_csv(file_name: str) -> List[Node]:
    nodes = []
    # first the file is opened
    with open(file_name, 'r') as file:
        # then the file is read
        reader = csv.reader(file)
        # now we go line by line inputting the data into a new Node
        for row in reader:
            node = Node()
            node.siteID = row[0]
            node.year_month = int(row[1])
            node.nitrogen = float(row[2])
            # Here the new Node is added to the array of nodes
            nodes.append(node)
    return nodes


# Function to visualize sorting steps
def visualize_sorting(nodes: List[Node], algorithm: str, sort_by: str):
    st.write(f"Sorting by {sort_by.capitalize()} using {algorithm} sort")

    start_time = time.time()
    # Here are the different ways of sorting
    # one option for the sorting is merge sort
    if algorithm == "Merge":
        # and it can sort by year or nitrogen values
        if sort_by == "year":
            merge_sort(nodes, 0, len(nodes) - 1, "year")
        else:
            merge_sort(nodes, 0, len(nodes) - 1, "nitrogen")
    # another option in the menu is sorting by Shell sort
    elif algorithm == "Shell":
        # and it can also sort by year or nitrogen values
        if sort_by == "year":
            shell_sort_by_year_month(nodes, len(nodes))
        else:
            shell_sort(nodes, len(nodes))

    end_time = time.time()
    # here the final time for sorting is calculated
    sorting_time = end_time - start_time

    # Visualize sorted data
    df = pd.DataFrame([(node.siteID, node.year_month, node.nitrogen) for node in nodes],
                      columns=['Site ID', 'Year/Month', 'Nitrogen Concentration (mg/L)'])
    st.write(df)
    st.write(f"Sorting time: {sorting_time:.4f} seconds")
    st.write("Nodes at the beginning and end of sorted data:")
    st.write(
        f"Smallest Node: Site ID: {nodes[0].siteID}, Year and Month: {nodes[0].year_month}, Nitrogen: {nodes[0].nitrogen}")
    st.write(
        f"Largest Node: Site ID: {nodes[-1].siteID}, Year and Month: {nodes[-1].year_month}, Nitrogen: {nodes[-1].nitrogen}")
    # this appears when the sorting is finished to celebrate
    st.balloons()
    st.success('Success!', icon="🌱")


# Function to display Streamlit UI
def menu():
    st.title("Nitro Navigator 🌱💧")
    st.header("Understanding Nitrogen Deposition")
    st.write("""💧 Nitrogen deposition refers to the process by which nitrogen compounds from the atmosphere 
    are deposited onto the Earth's surface, impacting ecosystems and the environment. It includes 
    both wet deposition (nitrogen compounds brought down by precipitation) and dry deposition 
    (nitrogen compounds directly deposited from the air). 
    """)
    st.write("""🌱 Nitrogen deposition is an important area of interest for agricultural specialists and those with an 
    interest in farming and land management. Currently, research is being done to assess where nitrogen deposition data collection sites should be located in the United States, 
    as well as the long and short-term effects of nitrogen deposition in the United States.""")
    st.write("""🔥 This web application helps analyze data related to nitrogen concentrations and provides insights 
    into the impact of nitrogen deposition on various parts of the United States. We have collected weekly nitrogen deposition data from the National Trends Network from 1978 to 2023.""")
    st.write("""🌀 Explore our sorting tools below to sort nitrogen deposition data by 
    year and month, or by nitrogen concentration in milligrams per liter. Select between merge sort, shell sort, or see both to compare the efficiency of the algorithms.""")
    # Here is the drop down menu where the user choses what to sort by
    sort_by = st.selectbox("Sort by", ["Year/Month", "Nitrogen Concentration"])
    # Here is the other drop down menu where the user chooses which sort
    sorting_algorithm = st.selectbox("Select sorting algorithm", ["Merge Sort", "Shell Sort", "See Both Sorts"])

    nodes = read_csv("NTN_data_cleaned_final.csv")

    if st.button("Sort"):
        st.write("Sorting... Please wait.")
        # the user can choose between year and month to sort by
        if sort_by == "Year/Month":
            # then they also choose between merger sort, shell sort,
            # Or they can choose both to get a comparison
            if sorting_algorithm == "Merge Sort":
                visualize_sorting(nodes.copy(), "Merge", "year")
            elif sorting_algorithm == "Shell Sort":
                visualize_sorting(nodes.copy(), "Shell", "year")
            else:  # See Both Sorts option
                nodes_copy = nodes.copy()
                visualize_sorting(nodes_copy, "Merge", "year")
                visualize_sorting(nodes, "Shell", "year")
        else:
            if sorting_algorithm == "Merge Sort":
                visualize_sorting(nodes.copy(), "Merge", "nitrogen")
            elif sorting_algorithm == "Shell Sort":
                visualize_sorting(nodes.copy(), "Shell", "nitrogen")
            else:  # See Both Sorts option
                nodes_copy = nodes.copy()
                visualize_sorting(nodes_copy, "Merge", "nitrogen")
                visualize_sorting(nodes, "Shell", "nitrogen")

    st.write(
        """💡 To read more about the research project which inspired this web application, the applications of this data, and the future of nitrogen deposition data collection, check out the link below!""")
    st.markdown(
        """###### [Click here to read more about research initiatives from UF IFAS](https://docs.google.com/presentation/d/1rqPIKZzqMGsGKaxnO4BHcBUoNtF16AlM/edit?usp=sharing&ouid=115915295533510389711&rtpof=true&sd=true) """)
    st.write("""💻 Project built by Tanya Charan, Teji Kari, and Gabriella Smith""")


if __name__ == "__main__":
    menu()



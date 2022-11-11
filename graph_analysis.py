import http.client
import requests
import json
import csv


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV] # tuple (id, name)

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str):
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        if (str(id), str(name)) not in self.nodes:
            self.nodes.append((str(id), str(name)))


    def add_edge(self, source: str, target: str):
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        if (str(source), str(target)) not in self.edges and (str(target), str(source)) not in self.edges:
            self.edges.append((str(source), str(target)))


    def total_nodes(self):
        """
        Returns an integer value for the total number of nodes in the graph
        """
        tot_nodes = len(self.nodes)
        return tot_nodes


    def total_edges(self):
        """
        Returns an integer value for the total number of edges in the graph
        """
        tot_edges = len(self.edges)graph = Graph()
graph.add_node(id='2975', name='Laurence Fishburne') # initialize graph nodes with Laurence

tmdb = TMDBAPIUtils(api_key='c9c25c7a1882c2724208e5f51f346a64')
person_list = tmdb.get_movie_credits_for_person(person_id='2975', vote_avg_threshold=8.0) # get all the movie credit ids in wich Laurence acted
movie_credits = [i['id'] for i in person_list]
# print(movie_credits)

for credit in movie_credits:
    cast_list = tmdb.get_movie_cast(movie_id=str(credit), limit=3, exclude_ids=[2975])

    for cast in cast_list:
        graph.add_node(id=cast['id'], name=cast['name'].replace(',', ' '))
        graph.add_edge(source='2975', target=cast['id'])

tot_nodes = graph.total_nodes() # number of nodes in base graph
for iter in range(0, 2):
    if iter == 0:
        nodes = graph.nodes[1:tot_nodes]
        node_ids = [node[0] for node in nodes]

    else:
        nodes = graph.nodes[tot_nodes:]
        node_ids = [node[0] for node in nodes]
    
    for id in node_ids:
        person_list = tmdb.get_movie_credits_for_person(person_id=str(id), vote_avg_threshold=8.0)
        movie_credits = [m['id'] for m in person_list]
    
        for credit in movie_credits:
            cast_list = tmdb.get_movie_cast(movie_id=str(credit), limit=3, exclude_ids=[int(id)])

            for cast in cast_list:
                graph.add_node(id=cast['id'], name=cast['name'].replace(',', ' '))
                graph.add_edge(source=str(id), target=cast['id'])

# k = graph.get_k()
# print(k)

graph.write_edges_file()
graph.write_nodes_file()
        return tot_edges


    def max_degree_nodes(self):
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        reversed_edges = [(i[1], i[0]) for i in self.edges]
        combined_edges = set(self.edges).union(set(reversed_edges))
        
        source_list = [i[0] for i in combined_edges]

        count_dict = {i:source_list.count(i) for i in source_list}
        max_num_nodes = max(count_dict.values())

        max_nodes_dict = dict()
        for key, value in count_dict.items():
            if value == max_num_nodes:
                max_nodes_dict[key] = value

        return max_nodes_dict


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    def write_edges_file(self, path="/data/edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    def write_nodes_file(self, path="/data/nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


    def get_k(self):
        """
        get number of edges that have more than 1 edge
        """
        reversed_edges = [(i[1], i[0]) for i in self.edges]
        combined_edges = set(self.edges).union(set(reversed_edges))
        
        source_list = [i[0] for i in combined_edges]

        count_dict = {i:source_list.count(i) for i in source_list}

        k_nodes_list = []
        for key, value in count_dict.items():
            if value > 1:
                k_nodes_list.append(key)
        return len(k_nodes_list)


class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None):
        response = requests.get('https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits?api_key=' + str(self.api_key) + '&language=en-US')
        movie_data = response.json()

        movie_list = []
        if exclude_ids == None:
            exclude_ids = []

        if 'cast' in movie_data.keys():
            if limit != None:
                i = 0
                while i < int(limit) and i < len(movie_data['cast']):
                    movie_dict = dict()
                    if int(movie_data['cast'][i]['id']) not in exclude_ids:
                        movie_dict['id'] = movie_data['cast'][i]['id']
                        movie_dict['character'] = movie_data['cast'][i]['character']
                        movie_dict['credit_id'] = movie_data['cast'][i]['credit_id']
                        movie_dict['name'] = movie_data['cast'][i]['name']
                        movie_list.append(movie_dict)
                    else: pass
                    i += 1
            else:
                i = 0
                while i < len(movie_data['cast']):
                    movie_dict = dict()
                    if int(movie_data['cast'][i]['id']) not in exclude_ids:
                        movie_dict['id'] = movie_data['cast'][i]['id']
                        movie_dict['character'] = movie_data['cast'][i]['character']
                        movie_dict['credit_id'] = movie_data['cast'][i]['credit_id']
                        movie_dict['name'] = movie_data['cast'][i]['name']
                        movie_list.append(movie_dict)
                    else: pass
                    i += 1

        return movie_list


    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None):
        response = requests.get('https://api.themoviedb.org/3/person/' + str(person_id) + '/movie_credits?api_key=' + str(self.api_key) + '&language=en-US')
        person_data = response.json()

        person_list = []

        if vote_avg_threshold:
            vote_avg_threshold = float(vote_avg_threshold)
        else:
            vote_avg_threshold = 0.0
        
        i = 0
        while i < len(person_data['cast']):
            person_dict = dict()
            if ('vote_average' not in person_data['cast'][i].keys()) or (person_data['cast'][i]['vote_average'] < vote_avg_threshold):
                pass
            else:
                person_dict['id'] = person_data['cast'][i]['id']
                person_dict['title'] = person_data['cast'][i]['title']
                person_dict['vote_avg'] = person_data['cast'][i]['vote_average']
                person_list.append(person_dict)
            i += 1

        return person_list



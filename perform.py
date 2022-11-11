import graph_analysis

# Use Graph() class of graph_analysis.py
graph = graph_analysis.Graph()
graph.add_node(id='2975', name='Laurence Fishburne') # initialize graph nodes with Laurence

tmdb = TMDBAPIUtils(api_key= ) # input a valid api_key
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
# Wiki_Editor_War
-----Setting:
	anaconda python3.6
	install plotly

----- Dataset:
     Put all article information to input/fa/

-----Code File:
     Form_Cluster_Chain_Files: 
                 1: Generate the new dataset, one is cluster, one is chain.
							   2: It read the input/fa/ fold and put all new dataset to output/ fold
                 
						chain:
								'title',
								'start_time',
								'end_time',
								'duration',
								'longest_revert_interval',
								'shortest_revert_interval',
								'medium_revert_interval',
								'number_of_reverts',
								'number_of_anonymous_reverts',
								'number_of_unique_registered_users',
								'Category'

						cluster:
								'title',
								'group_range',
								'start_time',
								'end_time',
								'duration',
								'longest_revert_interval',
								'shortest_revert_interval',
								'medium_revert_interval',
								'number_of_chains',
								'number_of_reverts',
								'number_of_anonymous_reverts',
								'number_of_unique_registered_users',
								'longest_chain_duration',
								'shortest_chain_duration',
								'medium_chain_duration',
								'most_number_reverted',
								'medium_number_reverted',
								'min_number_reverted','Category'
	
	Single_Article_Vis: Using plotly generate a single article figure.
	Total_Cluster_Chain_Vis: Using the new dataset.

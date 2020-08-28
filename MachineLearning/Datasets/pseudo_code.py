

LINES_TO_READ = 500000

SKIP_LINES = 0

while True :

	dataset = read_csv_per_chunk('/path/to/dataset.csv', lines=LINE_TO_READ, skip=SKIP_LINES)

	if dataset != None :

		unwanted_lines = search_lignes_contains_null_inf_values(dataset)

		delete_lines(dataset, unwanted_lines)

		duplicat_lines = search_duplicat_lines(dataset)

		delete_lines(dataset, duplicat_lines)

		save_and_append_in_new_file('/path/to/clean_dataset.csv', dataset)

		SKIP_LINES = SKIP_LINES + LINES_TO_READ

	else :

		break


"""
	list of all flows
"""
flows_list = []

"""
	method that receive the packet
"""
receive_packet (packet) :

	flow_id = generate_flow_id(packet)

	if (flow_id in flows_list) :

		new_flow = new Flow(flow_id)

		new_flow.flow_duration = 0

		new_flow.first_packet_time = time.now()

		flows_list[flow_id] = new_flow
	else :

		calculate_flow_duration(flow_id, packet)

"""
	flow_duration method
"""
calculate_flow_duration(packet) :

	flows_list[flow_id].flow_duration = time.now() - flows_list[flow_id].first_packet_time
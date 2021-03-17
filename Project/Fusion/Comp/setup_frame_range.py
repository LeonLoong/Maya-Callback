import os

project_path_map = list(comp.GetCompPathMap(False, False).values())[0]
folder_name_list = [folder for folder in os.listdir(project_path_map) if os.path.isdir(os.path.join(project_path_map, folder))]

frame_range_dict = {}
start_frame_list = []
end_frame_list = []

# get start and end frame by os 
for folder_name in folder_name_list:
	folder_path_list = (os.path.join(project_path_map, folder_name))
	if (os.listdir(folder_path_list)) != []:
		start_frame_file_name = (os.listdir(folder_path_list)[0])
		end_frame_file_name = (os.listdir(folder_path_list)[-1])

		if start_frame_file_name.split(".")[-2].isdigit() and end_frame_file_name.split(".")[-2].isdigit():
			start_frame = (start_frame_file_name.split(".")[-2])
			end_frame = (end_frame_file_name.split(".")[-2])
			frame_range_dict[folder_name] = [start_frame, end_frame]
			start_frame_list.append(start_frame)
			end_frame_list.append(end_frame)
		
# get timeline frame range
start_frame = int(min(start_frame_list))
end_frame = int(max(end_frame_list))

# set timeline frame range 
comp.SetAttrs({'COMPN_GlobalStart' : start_frame})
comp.SetAttrs({'COMPN_GlobalEnd' : end_frame})
comp.SetAttrs({'COMPN_RenderStart': start_frame})
comp.SetAttrs({'COMPN_RenderEnd': end_frame})

comp.Lock()

for loader in (comp.GetToolList(False, "Loader").values()):
	loader_path = loader.GetAttrs("TOOLST_Clip_Name")[1]
	loader_name = (loader_path.split("\\")[1])
	folder_path = ("{}\{}".format(project_path_map, loader_name))
	attrs = loader.GetAttrs()
	start_time = attrs["TOOLNT_Clip_Start"][1]
	end_time = attrs["TOOLNT_Clip_End"][1]
	loader.Clip[start_time] = loader.Clip[start_time]
	
	print (start_time, end_time, loader_name)
	if start_time == end_time:
		loader.Loop = 1
	else:
		loader.Loop = 0
	
comp.Unlock()

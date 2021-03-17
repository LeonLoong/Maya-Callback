{
	// ModifyDuration.jsx
	// 
	// This script modify composition.
	//
    // Todo: auto replace file
    //

    var root = 'X:\\Demo\\\data\\60_SHOT'
    var episode = 'ep1006'
    var sequence = 's007'
    var shot = 'c189'
    //var version = 'v99'
    //var increment = '99'
    //var name = episode + '_' + sequence + '_' + shot + '_' + 'composite' + '_' + version + '_'  + increment
    //var path = root + '\\' + episode + '\\' +sequence + '\\'  + shot + '\\' + 'compo' + '\\' + name + '.aep';
    var ch_directory = root + '\\' + episode + '\\' +sequence + '\\'  + shot + '\\' + 'compo' + '\\' + 'Layer\\CH\\';
    
    var end_frame_list = [];

    function ReplaceFootageItem() {
        for (var i = 1; i <= app.project.items.length; i++) {
            if (app.project.item(i).name == 'element') {
                for (var j = 1; j <= app.project.item(i).items.length; j++) {
                    if (app.project.item(i).items[j].name == 'CH') {
                        for (var k = 1; k <= app.project.item(i).items[j].items.length; k++) {
                            for (var x = 1; x <= app.project.item(i).items[j].items[k].items.length; x++) {
                                for (var y = 1; y <= app.project.item(i).items[j].items[k].items[x].items.length; y++) {
                                    var replace_target_path = (app.project.item(i).items[j].items[k].items[x].items[y].file.fsName);
                                    var replace_target = (app.project.item(i).items[j].items[k].items[x].items[y]);
                                    // get all version in directory
                                    var version_directory = new Folder(ch_directory + (app.project.item(i).items[j].items[k].items[x].parentFolder.name + ('\\') + app.project.item(i).items[j].items[k].items[x].items[y].parentFolder.name)).getFiles();
                                    try {
                                        var front_directory = version_directory[version_directory.length - 1].fsName
                                        var back_directory = replace_target_path.split('\\')[replace_target_path.split('\\').length -2] + '\\' + (replace_target_path.split('\\')[replace_target_path.split('\\').length -1].replace('0001', '0101'));
                                        var replace_source = new File(front_directory + '\\' + back_directory);
                                        // currently replace with placeHolder to prevent sohai bug.
                                        replace_target.replaceWithPlaceholder('placeHolder',1536, 864, 24, 0);
                                        replace_target.replaceWithSequence(replace_source, false) ;
                                        var end_frame = (replace_target.name.split('.')[1].split('-')[1].replace(/\D+/g, ''));
                                        end_frame_list.push(end_frame);
                                    } catch(error) {
                                        // pass
                                    }  
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // issues: need press 2 time to get expected result
    // usage: ModifyDuration(duration); duration = int
    function ModifyDuration() {
        duration = (Math.max.apply(null, end_frame_list));
        // (frame / frame per second = seconds)
		for (var i = 1; i <= app.project.numItems; i ++) {
            if (app.project.item(i) instanceof CompItem){
                comp = app.project.item(i);
                comp.duration = (duration/24);
                for (var j = 1; j <= app.project.item(i).numLayers; j ++) {
                    layer = app.project.item(i).layer(j);
                    try {             
                        layer.inPoint = (0/24);
                        layer.outPoint = (duration/24);
                    } catch(error) {
                        // pass
                    }
                }
            }
        }
    }

    // issues: need press 2 time to get expected result
    // usage: ModifyDuration(duration); duration = int
    function ManualModifyDuration(duration) {
        // (frame / frame per second = seconds)
		for (var i = 1; i <= app.project.numItems; i ++) {
            if (app.project.item(i) instanceof CompItem){
                comp = app.project.item(i);
                comp.duration = (duration/24);
                for (var j = 1; j <= app.project.item(i).numLayers; j ++) {
                    layer = app.project.item(i).layer(j);
                    try {             
                        layer.inPoint = (0/24);
                        layer.outPoint = (duration/24);
                    } catch(error) {
                        // pass
                    }
                }
            }
        }
    }

//ReplaceFootageItem();
//ModifyDuration();
ManualModifyDuration(230);

    // save file to specified folder
    function SaveFile() {
        // save file to specified folder
        app.project.save(File(path));
    }
    //SaveFile();
    
}
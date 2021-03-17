{
	// ModifyDuration.jsx
	// 
	// This script modify selected composition.
	//
	
	function ModifyDuration(thisObj)
	{
		var scriptName = "Modify Duration";
		
		// This variable stores the duration_factor.
		var text_input = null;

		//
		// This function is called when the user enters text for the scale.
		//
		function on_textInput_changed()
		{
            var value = this.text;            
            duration_factor = value;
		}
		
		
		function onScaleClick()
		{
            // Validate the input field, in case the user didn't defocus it first (which often can be the case).
            this.parent.parent.optsRow.text_input.notify("onChange");
           
            // By bracketing the operations with begin/end undo group, we can 
            // undo the whole script with one undo operation.
            app.beginUndoGroup(scriptName);
            
            // Set new comp width and height.	
            var proj = app.project;
            for (var i = 1; i <= app.project.numItems; i ++) {
                if (app.project.item(i) instanceof CompItem){
                    comp = app.project.item(i);
                    comp.duration = (duration_factor/24);
                    for (var j = 1; j <= app.project.item(i).numLayers; j ++) {
                        layer = app.project.item(i).layer(j);
                        try {             
                            layer.inPoint = (0/24);
                            layer.outPoint = (duration_factor/24);
                        } catch(error) {
                            // pass
                        }
                    }
                }
            }
            
            app.endUndoGroup();

		}
		
		
		// 
		// This function puts up a modal dialog asking for a duration_factor.
		// Once the user enters a value, the dialog closes, and the script scales the comp.
		// 
		function BuildAndShowUI(thisObj)
		{
			// Create and show a floating palette.
			var my_palette = (thisObj instanceof Panel) ? thisObj : new Window("palette", scriptName, undefined, {resizeable:true});
			if (my_palette != null)
			{
				var res = 
					"group { \
						orientation:'column', alignment:['fill','top'], alignChildren:['left','top'], spacing:5, margins:[0,0,0,0], \
						introStr: StaticText { text:'Total Frame:', alignment:['left','center'] }, \
						optsRow: Group { \
							orientation:'column', alignment:['fill','top'], \
							text_input: EditText { text:'1', alignment:['left','top'], preferredSize:[80,20] }, \
						}, \
						cmds: Group { \
							alignment:['fill','top'], \
							okButton: Button { text:'Modify', alignment:['fill','center'] }, \
						}, \
					}";
				
				my_palette.margins = [10,10,10,10];
				my_palette.grp = my_palette.add(res);
				
				// Workaround to ensure the edittext text color is black, even at darker UI brightness levels.
				var winGfx = my_palette.graphics;
				var darkColorBrush = winGfx.newPen(winGfx.BrushType.SOLID_COLOR, [0,0,0], 1);
				my_palette.grp.optsRow.text_input.graphics.foregroundColor = darkColorBrush;
				
				// Set the callback. When the user enters text, this will be called.
				my_palette.grp.optsRow.text_input.onChange = on_textInput_changed;
				
				my_palette.grp.cmds.okButton.onClick = onScaleClick;
				
				my_palette.onResizing = my_palette.onResize = function () {this.layout.resize();}
			}
			
			return my_palette;
		}
		
		// 
		// The main script.
		//
		if (parseFloat(app.version) < 8) {
			alert("This script requires After Effects CS3 or later.", scriptName);
			return;
		}
		
		var my_palette = BuildAndShowUI(thisObj);
		if (my_palette != null) {
			if (my_palette instanceof Window) {
				my_palette.center();
				my_palette.show();
			} else {
				my_palette.layout.layout(true);
				my_palette.layout.resize();
			}
		} else {
			alert("Could not open the user interface.", scriptName);
		}
	}
	
	ModifyDuration(this);
}
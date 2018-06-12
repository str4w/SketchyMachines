def help():
   print """
http://sites.music.columbia.edu/cmc/chiplotle/manual/chapters/api/plotters.html
actual_position - Output the actual position of the plotter pen. Returns a 
                  tuple (Coordinate(x, y), pen status)
advance_frame()
advance_full_page()
advance_half_page()
carousel_type
clear() - Tells the virtual serial port to forget its stored commands. 
          Used to "erase" the drawing on the virtual plotter.
clear_digitizer()
commanded_position - Output the commanded position of the plotter pen. Returns
                     a tuple [Coordinate(x, y), pen status]
digitize_point()
digitized_point - Returns last digitized point. Returns a tuple 
                  [Coordinate(x, y), pen status]
enable_cut_line(n)
escape_plotter_on()
format - This lets us pass the VirtualPlotter directly to io.view() Returns 
         None if called on a plotter with a real serial port.
goto(*args) - Alias for PA( ) with only one point. Pass in either an x, y pair:
              goto(100, 100) or a tuple pair: goto((x, y)) or a 
              Coordinate: goto(Coordinate(100,100))
goto_bottom_left()
goto_bottom_right()
goto_center()
goto_origin()
goto_top_left()
goto_top_right()
id - Get id of plotter. Returns a string.
initialize_plotter()
label_length
margins - Read-only reference to MarginsInterface.
nudge(x, y)
options
output_error
output_key
output_p1p2 - Returns the current settings for P1, P2. Returns two Coordinates
page_feed(n=None)
pen_down(coords=None)
Pen Down.
pen_up(coords=None)
Pen Up.
replot(n=1)
rotate(angle=0)
scale(xMin, xMax, yMin, yMax)
select_pen(penNum=0)
set_origin_bottom_left()
Set origin to bottom, left
set_origin_bottom_right()
Set origin to bottom, right
set_origin_center()
Set origin to center, center
set_origin_current_location()
Set origin to current location
set_origin_to_point(point)
Set origin to given point [x, y]
set_origin_top_left()
Set origin to upper, left
set_origin_top_right()
Set origin to top, right
set_plot_window(left_bottom, right_top) - Programatically set new margins 
                                          for the plotting window. Arguments 
                                          must be two tuple pairs (x, y) or 
                                          two Coordinates.
status
write(data) - Public access for writing to serial port. data can be an 
              iterator, a string or an _HPGL.
write_file(filename) - Sends the HPGL content of the given filename to the 
                       plotter.
"""

def square(plotter,x,y,dx,dy):
   plotter.pen_up([(x,y)])
   plotter.pen_down([(x,y),(x+dx,y),(x+dx,y+dy),(x,y+dy),(x,y)])
   plotter.pen_up()


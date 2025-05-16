from plotter import Plotter
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
##INIT##
config = Plotter.get_config_variables()

#####PARAMETER#####
region = 3
layer_id = 5
#time= add_z_if_needed("2024-10-01T00:00:00Z")
resolution = "l"
#####PARAMETER#####

layer_map_data = Plotter.fetch_wms_layer_data(layer_id)

#REMOVE DEMO
time = Plotter.demo_time(layer_map_data)
#REMOVE DEMO
#####MAIN#####
dap_url, dap_variable = Plotter.get_dap_config(layer_map_data)
title, dataset_text = Plotter.get_title(layer_map_data,time)
cmap_name, plot_type, min_color_plot, max_color_plot, steps, units, levels, discrete = Plotter.get_plot_config(layer_map_data)
west_bound, east_bound, south_bound, north_bound, country_name, short_name = Plotter.getBBox(region)
eez_url = Plotter.getCountryData(region)

##PLOTTING
figsize = Plotter.cm2inch((15,13))
fig, ax = plt.subplots(figsize=figsize, dpi=300)
ax.axis('off')

ax2 = fig.add_axes([0.09, 0.2, 0.8, 0.65])
title = "%s \n %s" % (country_name,title)
ax2.set_title(title, pad=10, fontsize=8)

m = Basemap(projection='cyl', llcrnrlat=south_bound, urcrnrlat=north_bound, 
            llcrnrlon=west_bound, urcrnrlon=east_bound, resolution=resolution, ax=ax2)

Plotter.plot_map_grid(m, south_bound, north_bound, west_bound, east_bound,region)

# Add colorbar to ax2
ax2_pos = ax2.get_position()
ax_legend_width = 0.03  # Width of the legend
ax_legend_gap = 0.1    # Gap between ax2 and ax_legend
ax_legend = fig.add_axes([ax2_pos.x1 +0.02, ax2_pos.y0, ax_legend_width, ax2_pos.height])



##MAIN PLOTTER
if plot_type == "contourf":
    lon, lat, data_extract = Plotter.getfromDAP(dap_url, time, dap_variable,adjust_lon=True)
    cs, cbar = Plotter.plot_filled_contours(ax=ax2, ax_legend=ax_legend, lon=lon, lat=lat, data=data_extract,\
        min_color_plot=min_color_plot, max_color_plot=max_color_plot, steps=steps, cmap_name=cmap_name, units=units
    )
elif plot_type == "contourf_nozero":
    lon, lat, data_extract = Plotter.getfromDAP(dap_url, time, dap_variable,adjust_lon=True)
    cs, cbar = Plotter.plot_filled_contours_no_zero(ax=ax2, ax_legend=ax_legend, lon=lon, lat=lat, data=data_extract,\
        min_color_plot=min_color_plot, max_color_plot=max_color_plot, steps=steps, cmap_name=cmap_name, units=units
    )
elif plot_type == "pcolormesh":
    lon, lat, data_extract = Plotter.getfromDAP(dap_url, time, dap_variable,adjust_lon=True)
    cs, cbar = Plotter.plot_filled_pcolor(ax=ax2, ax_legend=ax_legend, lon=lon, lat=lat, data=data_extract,\
        min_color_plot=min_color_plot, max_color_plot=max_color_plot, steps=steps, cmap_name=cmap_name, units=units
    )
elif plot_type == "wave_with_dir":
    wave_height_varib, wave_dir_varib = dap_variable.split(',')
    lon, lat, wave_height = Plotter.getfromDAP(dap_url, time, wave_height_varib, adjust_lon=True)
    _, _, wave_dir = Plotter.getfromDAP(dap_url, time, wave_dir_varib, adjust_lon=True)
    step = 10
    if int(region) == 1:
        step = 30
    cs, q, cbar = Plotter.plot_wave_field(ax2, ax_legend, m, lon, lat, wave_height, wave_dir,\
                            min_color_plot, max_color_plot, steps,region, step, cmap_name=cmap_name, units=units)
elif plot_type == "discrete":
    lons, lats, bleaching_data = Plotter.getfromDAP(dap_url, time, dap_variable, adjust_lon=True)
    splitBy_ = discrete.split("_")
    if len(splitBy_) > 1:
        colors = splitBy_[0]
        split_1 = splitBy_[1]
        range_nums, range_name = split_1.split('%')
        color_arr = np.array(eval(colors), dtype=str)
        range_nums_arr = np.array(eval(range_nums), dtype=str)
        range_name_arr = np.array(eval(range_name), dtype=str)

        cs, cbar = Plotter.plot_discrete_map_ranges(ax=ax2, ax_legend=ax_legend, lons=lons, lats=lats, bleaching_data=bleaching_data,\
            cmap_colors=color_arr, colorbar_labels=range_name_arr, ranges=range_nums_arr)
    else:
        tmp_color, tmp_label = discrete.split('-')
        color_arr = np.array(eval(tmp_color), dtype=str)
        label_arr = np.array(eval(tmp_label), dtype=str)

        cs, cbar = Plotter.plot_discrete_map(ax=ax2, ax_legend=ax_legend, lons=lons, lats=lats, bleaching_data=bleaching_data,\
            cmap_colors=color_arr, colorbar_labels=label_arr)

elif plot_type == "levels_pcolor":
    lons, lats, chl_data = Plotter.getfromDAP(dap_url, time, dap_variable, adjust_lon=True)
    Plotter.plot_levels_pcolor(ax2, ax_legend, lons, lats, chl_data,cmap_name, units=units,levels=levels)

elif plot_type == "levels_contourf":
    lons, lats, chl_data = Plotter.getfromDAP(dap_url, time, dap_variable, adjust_lon=True)
    Plotter.plot_levels_contour(ax2, ax_legend, lons, lats, chl_data,cmap_name, units=units,levels=levels,)

elif plot_type == "climate":
    split_varib = dap_variable.split(",")
    lon, lat, data_extract = Plotter.getfromDAP(dap_url, time, split_varib[0],adjust_lon=True)
    cs, cbar = Plotter.plot_climatology(dap_url,time,ax=ax2, ax_legend=ax_legend, lon=lon, lat=lat, data=data_extract,\
        min_color_plot=min_color_plot, max_color_plot=max_color_plot, steps=steps, cmap_name=cmap_name, units=units
    )
elif plot_type == "currents":
    lon, lat, uo = Plotter.getfromDAP(dap_url, time, 'uo', adjust_lon=True)
    _, _, vo = Plotter.getfromDAP(dap_url, time, 'vo', adjust_lon=True)
    pcm, quiv, cbar = plot_current_magnitude(
        ax=ax2,
        ax_legend=ax_legend,
        lon=lon,
        lat=lat,
        uo=uo,
        vo=vo,
        region=region,
        min_color_plot=min_color_plot,
        max_color_plot=max_color_plot,
        steps=0.1,
        cmap_name=cmap_name,
        units=units,
        show_arrows=True,
        arrow_scale=3,      # Replaces arrow_size (higher = bigger arrows)
        density=50,          # More arrows than before (since we're scaling by magnitude)
        arrow_color='white',  # Options: color string, or 'magnitude' to color by speed
        min_speed=0.05       # Hide very weak currents (adjust based on your data range)
    )


#ADD LOGO AND FOOTER
Plotter.add_logo_and_footer(fig=fig, ax=ax, ax2=ax2, ax2_pos=ax2_pos, region=1, copyright_text=config.copyright_text,\
    footer_text=config.footer_text,dataset_text=dataset_text)

#PLOT EEZ
Plotter.getEEZ(ax2,eez_url,m)

Plotter.plot_coastline_from_geoserver(ax2,m)
Plotter.plot_city_names(ax2,m,short_name)


plt.savefig('anuj3.png', bbox_inches='tight', pad_inches=0.1,dpi=300)
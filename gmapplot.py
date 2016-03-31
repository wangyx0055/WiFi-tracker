import gmplot

gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

more_lats = [37.428,37.4319744,37.4272119]
more_lngs = [-122.1471887,-122.1451771,-122.1378493]

#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)


gmap.plot(more_lats, more_lngs, 'big bubu', edge_width=10)
#gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap7.html")

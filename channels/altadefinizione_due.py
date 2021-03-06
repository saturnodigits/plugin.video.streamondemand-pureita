# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale per il sito altadefinizione_due
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# creato by Robin
#  - il mio primo canale - grazie per l'aiuto :) -
# -------------------------------------------------------------------
import re
import urlparse

from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altadefinizione_due"
host = "http://altadefinizione2.com"

headers = [['Referer', host]]

def mainlist(item):
    logger.info("[streamondemand-pureita altadefinizione_due ] mainlist")
	
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Aggiornati[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Votati[/COLOR]",
                     action="peliculas",
                     url=host + "/film-piu-votati/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Popolari[/COLOR]",
                     action="peliculas",
                     url=host + "/film-piu-popolari/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film[COLOR orange] - Animazione[/COLOR]",
                     action="peliculas",
                     url=host + "/category/animazione/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

	
# ===================================================================================================================================================
	
def categorias(item):
    logger.info("[streamondemand-pureita altadefinizione_due ] categorias")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<h2>Categorie</h2>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)" >([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:    
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

	
# ===================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita altadefinizione_due ] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

		
# ===================================================================================================================================================
	
def peliculas(item):
    logger.info("[streamondemand-pureita altadefinizione_due ] peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="moviefilm">\s*<a href="([^"]+)">\s*<span class="tr-dublaj">'
    patron += '</span>\s*<img src="([^"]+)" alt="(.*?)"\s*height[^>]+>\s*</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace(":", " - ").replace(" Streaming", "")
        scrapedtitle = scrapedtitle.replace("streaming hd", "").replace("&#038;", "e")
        scrapedtitle = scrapedtitle.replace("[sub-ita]", " [[COLOR yellow]Sub-ITA[/COLOR]]")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl + "2",
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo="movie"))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" href="([^"]+)">&raquo;</a>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

	
# ===================================================================================================================================================
	
def find_movie(item):
    logger.info("[streamondemand-pureita altadefinizione_due ] findvideos_movie")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<span>HD.*?<a\s*href="([^"]+)">.*?<span>([^<]+)<\/span>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title="Play con " + "[COLOR orange]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 fulltitle=scrapedtitle,
                 plot=item.plot,
                 show="[COLOR azure]" + item.title + "[/COLOR] - " + scrapedtitle))
				 
				 
    return itemlist

	
# ===================================================================================================================================================
'''
def findvideos(item):
    logger.info("[streamondemand-pureita altadefinizione_due ] findvideos")
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<p><iframe src="([^"]+)"[^>]+>.*?<\/iframe>.*?<\/p>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        data += httptools.downloadpage(scrapedurl).data
    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = "[COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)

    return itemlist'''
	
# ===================================================================================================================================================

def findvideos(item):
    logger.info("[streamondemand-pureita altadefinizione_due ] play")

    data = httptools.downloadpage(item.url, headers=headers).data

    path = scrapertools.find_single_match(data, '<p><iframe src="([^"]+)"[^>]+>')
    url = path
    location = scrapertools.get_header_from_response(url, header_to_get="Location")

    itemlist = servertools.find_video_items(data=location)

    for videoitem in itemlist:
        videoitem.title = item.title + "  [COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.fulltitle + videoitem.title
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist


# ===================================================================================================================================================
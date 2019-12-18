#---------------------------
import xml_file_loader
import utils_xml
#---------------------------
import os
from lxml import etree
import bottle
from bottle import redirect
from bs4 import BeautifulSoup

#parsing du fichier XML

"""
#marche pas a cause des '&' et des '#' qui font crash le parser

"""

def telecharge(author_name):
        file_name = author_name+".xml"
        list_file = os.listdir("Auteurs/")
        if(file_name not in list_file):
        #si le fichier n'existe pas on le telecharge
            status = utils_xml.download_file(author_name, "Auteurs/", "table_html.txt")
            if(status != 200):
                #error(status, message)
                print(status)
                return "erreur"
        return "ok"

#--------------------------FONCTION BOTTLE--------------------------


@bottle.route("/auteur/qui")
@bottle.view("page.tpl")
def auteur():
    stri = """
    <form method='post' action='name'>
    <input type='text' name='last_name' placeholder='Nom'/>
    <input type='text' name='first_name' placeholder='Prénom'/>
    <input type='submit' value='Chercher'/>
    </form>
    """
    return {"title":"Rechercher un auteur", "body":stri}



@bottle.route("/auteur/name", method='POST')
@bottle.view("page.tpl")
def name():
    lname = bottle.request.forms.last_name
    fname = bottle.request.forms.first_name
    redirect("/auteur/"+lname+"/"+fname)

@bottle.route("/auteur/<lname>/<name>")
@bottle.view("page.tpl")
def auteur(lname,name):
   
    author_name = name+" "+lname
    file_name = author_name+".xml"
    if telecharge(author_name)=="ok" :
        tab=xml_file_loader.publication_stat("Auteurs/"+file_name)
    else :
        return {"title":"Oups nous n'avons pas pu récupérer les information de cette personne", "body":""}
    dico=xml_file_loader.publication_stat("Auteurs/"+file_name)

    stri="""<div><table style="border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse">
    <caption>Statistiques générales</caption>
    <tr>
    <td style="border:1px solid black;padding:10px">Nombre de journaux</td>"""+"<td style='border:1px solid black;padding:10px'>"+str(dico["journaux"])+"""</td>
    </tr>
    <tr>
    <td style='border:1px solid black;padding:10px'>Nombre de conferences</td>"""+"<td style='border:1px solid black;padding:10px'>"+str(dico["conferences"])+"""</td>
    </tr>
    <tr>
    <td style='border:1px solid black;padding:10px'>Nombre de co-auteurs</td>"""+ "<td style='border:1px solid black;padding:10px'>"+str(dico["co-auteurs"])+"""</td>
    </tr>
    </table></div>"""
    
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}


@bottle.route("/auteur/Journals/synthese/<lname>/<name>")
@bottle.view("page.tpl")
def synthese(lname,name):
    
    author_name = name+" "+lname
    file_name = author_name+".xml"
    if telecharge(author_name)=="ok" :
        tab = xml_file_loader.liste_resume_publication("Auteurs/"+file_name)
    else :
        return {"title":"Oups nous n'avons pas pu récupérer les information de cette personne", "body":""}
    tmp="vide"

    stri="""<div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <caption>Publications</caption>
    <tr>
    <th style='border:1px solid black'>Annee</th>
    <th style='border:1px solid black'>Journal</th>
    </tr>"""

    for pub in tab:
        if tmp=="vide" or tmp[1]==pub[1]:
            pass
        else:
            stri+=" <tr><td style='border:1px solid black;padding:10px'>"+pub[0]+"</td><td style='border:1px solid black;padding:10px'>"+pub[1]+"</td></tr>"
        tmp=pub

    stri+="</table></div>"
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}


@bottle.route("/auteur/Journals/<lname>/<name>")
@bottle.view("page.tpl")
def journal(lname,name):
    author_name = name+" "+lname
    file_name = author_name+".xml"
    if telecharge(author_name)=="ok" :
        tab = xml_file_loader.liste_detail_publication("Auteurs/"+file_name)
    else :
        return {"title":"Oups nous n'avons pas pu récupérer les information de cette personne", "body":""}
    stri="""<div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <caption>Publications</caption>
    <tr>
    <th style='border:1px solid black'>Article</th>
    <th style='border:1px solid black'>Auteur</th>
    <th style='border:1px solid black'>Journal</th>
    <th style='border:1px solid black'>Annee</th>
    </tr>"""
    for pub in tab:
            stri+=" <tr><td style='border:1px solid black;padding:10px'>"+pub[0]+"</td><td style='border:1px solid black;padding:10px'>"+pub[1]+"</td>"
            stri+=" <td style='border:1px solid black;padding:10px'>"+pub[2]+"</td><td style='border:1px solid black;padding:10px'>"+pub[3]+"</td></tr>"

    stri+="</table></div>"
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}

#--------------------------FIN FONCTION BOTTLE--------------------------

if __name__ == '__main__':
    #--------------------------RUN BOTTLE--------------------------
    bottle.run(bottle.app(), host='localhost', port='8080', debug=True, reloader=True)
    #--------------------------RUN BOTTLE--------------------------

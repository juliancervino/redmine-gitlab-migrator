from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from urllib import request
from aiohttp.helpers import set_result
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json



class GqlClient:
    
    QUERY_GET_PAGE_X_ID = gql(
        """
        query pages ($id: Int!) {
        pages {
            single (id: $id) {
            id
            title
            description
            editor
            path
            }
        }
        }
    """
    )

    QUERY_GET_PAGE_X_PATH = gql(
        """
        query pages ($path: String!, $locale: String!, $mode: PageTreeMode!) {
        pages {
            tree (path: $path, locale: $locale, mode: $mode) {
                id
                path
                depth
                title
                isPrivate
                isFolder
                privateNS
                parent
                pageId
                locale
                }
            }
        }
    """
    )

    CREATE_PAGE = gql(
        """
        mutation pages ($content: String!, $description: String!, $editor: String!, $isPublished: Boolean!, $isPrivate: Boolean!, $locale: String!, $path: String!,  , $tags: [String]!, $title: String!) {
        pages {
            create (content: $content, description: $description, editor: $editor, isPublished: $isPublished, isPrivate: $isPrivate, locale: $locale, path: $path,  tags: $tags, title: $title) {
                responseResult {
                    succeeded
                    errorCode
                    slug
                    message
                }
                page {
                    id
                    path
                    title
                }
            }
        }
    }
    """
    )
    UPDATE_PAGE = gql(
        """
        mutation pages ($content: String!, $description: String!, $editor: String!, $isPublished: Boolean!, $isPrivate: Boolean!, $path: String!, $id: Int!, $tags: [String]!, $title: String!) {
        pages {
            update (id: $id, content: $content, description: $description, editor: $editor, isPrivate: $isPrivate, isPublished: $isPublished, path: $path, tags: $tags, title: $title) {
                responseResult {
                    succeeded
                    errorCode
                    slug
                    message
                }
                page {
                    id
                    path               
                    title
                    description
                    isPrivate
                    isPublished               
                    createdAt
                    updatedAt                                        
                    authorId
                    authorName
                    authorEmail
                    creatorId
                    creatorName
                    creatorEmail
                }
            }
        }
    }
    """
    )

    UPLOAD_ASSETS = gql(
        """
        mutation assets ($parentFolderId: Int!, $slug: String!, $name: String, $id: Int!, $filename: String!, $id1: Int!) {
        assets {
            createFolder (parentFolderId: $parentFolderId, slug: $slug, name: $name) {
                responseResult {
                    succeeded
                    errorCode
                    slug
                    message
                }
            }
            renameAsset (id: $id, filename: $filename) {
                responseResult {
                    succeeded
                    errorCode
                    slug
                    message
                }
            }
            deleteAsset (id: $id1) {
                responseResult {
                    succeeded
                    errorCode
                    slug
                    message
                }
            }
            flushTempUploads {
                responseResult {
                    succeeded
                    errorCode
                    slug
                    message
                }
            }
        }
    }"""
    )



    def __init__(self, url, api_key):
        token = "Bearer " + api_key
        transport = AIOHTTPTransport(url=url, headers={'Authorization': token})
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
    
    def get_page_x_id(self, page_id):
        params = {"id": page_id}    
        result = self.client.execute(GqlClient.QUERY_GET_PAGE_X_ID, variable_values=params)
        return result

    def get_page_x_path(self, path, locale):
        params = {"path": path, "locale": locale, "mode": "ALL"}    
        print(params)
        result = self.client.execute(GqlClient.QUERY_GET_PAGE_X_PATH, variable_values=params)
        return result


    def create_page(self, path, content, title, description, editor, locale, tags, isPublished, isPrivate):
        params = {
            "path": path,
            "content": content,
            "title": title,
            "description": description,
            "editor": editor,
            "locale": locale,
            "tags": tags,
            "isPublished": isPublished,
            "isPrivate": isPrivate
        }
        result = self.client.execute(GqlClient.CREATE_PAGE, variable_values=params)
        if (not result["pages"]["create"]["responseResult"]["succeeded"]):
            if (result["pages"]["create"]["responseResult"]["slug"]=="PageDuplicateCreate"):
                print("Página duplicada")
                print(result) 
            else:
                print(result)     
        return result
    
    def update_page(self, path, identificador, content, title, description, editor, locale, tags, isPublished, isPrivate):
        params = {
            "path": path,
            "id": identificador,            
            "content": content,
            "title": title,
            "description": description,
            "editor": editor,
            "locale": locale,
            "tags": tags,
            "isPublished": isPublished,
            "isPrivate": isPrivate
        }
        
        print("La página se está actualizando con id: "+str(identificador)+" y título "+str(title))
        

        pagina_actulizada = self.client.execute(GqlClient.UPDATE_PAGE, variable_values=params)                
        
        return pagina_actulizada
    
    def upload_assets(self, parentFolderId, slug, name):
        params = {
            "parentFolderId": parentFolderId,
            "slug": slug,
            "name": name                       
        }
        print("Cargando complementos")
        carga_complementos=self.client.execute(GqlClient.UPLOAD_ASSETS, variable_values=params)
        return carga_complementos


    def create_or_update_page(self, path, content, title, description, editor, locale, tags, isPublished, isPrivate):
        params = {
            "path": path,
            "content": content,
            "title": title,
            "description": description,
            "editor": editor,
            "locale": locale,
            "tags": tags,
            "isPublished": isPublished,
            "isPrivate": isPrivate,            
        }

        result = self.get_page_x_path(path, locale)    
        encontrado=False                 
        
        for i in result.values():

                tree=i      #print(tree) Devuelve un diccionario donde el valor almacenado es una lista con diccionarios

                for j in tree.values():

                    page_tree=j     #print(page_tree) Devuelve una lista donde cada elemento es un diccionario

                    for page in page_tree:

                        #print(json.dumps(k, sort_keys=False,indent=4))    Devuelve cada diccionario de la lista, nos interesa 'id' y 'path' en un formato json más legible                         
                       

                        if page["path"] == path:
                            print("La página existe y su id es "+str(page["pageId"])+" "+str(path))
                            encontrado=True
                            identificador=page["pageId"]                           

                            break                       
        
        if encontrado==True:

            print("Actualizando página "+str(identificador))
            actu=self.update_page(path, identificador, content, title, description, editor, locale, tags, isPublished, isPrivate)           
                   
        else:
            
            print("Creando nueva página")
            new=self.create_page(path, content, title, description, editor, locale, tags, isPublished, isPrivate)
           
                        
       

        #return result   
        

    # Hay que repasar la lista de resultados (si hay) comparando el path para quedarnos con el id de la página y poder hacer el update        
    # 1. Comprobamos si existe la página (misma ruta mismo título)
    # 1.1 Obtener las páginas que hay en esa ruta (no debería ser así, pero wiki.js no me proporciona otro método para buscar por ruta)
    # 1.2. Hay que repasar la lista de resultados (si hay) comparando el path para quedarnos con el id de la página y poder hacer el update
    # 1.2.1 Comprobamos si hay resultados
    # 1.2.2 Si no hay resultados -> pasamos a crear la página (llamamos al método create_page)
    # 1.2.3 Si hay resultados -> recorremos el diccionario de resultados y comparamos el path con el de la página que estamos intentando crear/actualizar
    # 1.2.4 Si encontramos en el diccionario la página que estamos intentando crear -> nos quedamos con el id de esa página y llamamos al método de update_page
    # 1.2.5 Si recorremos todo el diccionario y no encontramos la página -> pasamos a crear la página (llamamos al método create_page)
    #if (result["pages"]["tree"]["id"]):           

    #------Probando funciones-------#

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

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
            "isPrivate": isPrivate
        }

        result = self.get_page_x_path(path, locale)
        # Hay que repasar la lista de resultados (si hay) comparando el path para quedarnos con el id de la página y poder hacer el update
        #if (result["pages"]["tree"]["id"]):
        
        return result
        
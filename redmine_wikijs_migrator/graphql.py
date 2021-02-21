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
    
    def get_page(self,page_id):
        params = {"id": page_id}    
        result = self.client.execute(GqlClient.QUERY_GET_PAGE_X_ID, variable_values=params)
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
            print ("Error creating page in wikijs")
            print(result)     
        return result
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import networkx as nx
import requests


class DOMBuilder:

    def __init__(self):
        self._dfs_counter = 0
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
            "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
        }

    def traverse_html(self, _d, _graph, _parent=None):
        for i in _d.contents:
            if i.name is not None:
                try:
                    if _parent is not None:
                        _graph.add_node(_parent)
                        self._dfs_counter = self._dfs_counter + 1
                        _graph.add_edge(_parent, self._dfs_counter)
                    self.traverse_html(i, _graph, self._dfs_counter)
                except AttributeError:
                    pass

    def graph_builder(self, url):

        G = nx.Graph()
        response = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(response.content, "lxml")

        """Removes tags other than 'body' tag in html dom tree"""
        soup = soup.html
        for i in soup.children:
            if i.name != 'body':
                i.extract()
        soup.head.extract()
        for i in soup.body.children:
            if i.name != 'None':
                i.extract()
        for script in soup.select('script'):
            script.extract()

        node_dict = {}
        self.traverse_html(soup, G)
        # draw graph from networkx library
        # nx.draw(G, nx.planar_layout(G), node_size=20)
        # plt.savefig("vis.png")
        return G

    def graph_loader(self, url_list):
        # sample
        # url_list = ["https://website1649510.nicepage.io/Contact.html?version=3e4b754f-560c-4f11-a59a-f4eccf6f5e53"]
        graph_list = []
        for i in url_list:
            graph_list.append(self.graph_builder(i))

        return graph_list

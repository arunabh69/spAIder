from bs4 import BeautifulSoup
import networkx as nx
import requests
from collections import defaultdict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
    "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
}


def _traverse_html(_d, _graph, _counter, _parent=None, _node_dict=None):
    for i in _d.contents:
        if i.name is not None:
            try:
                _name_count = _counter.get(i.name)
                if _parent is not None:
                    _graph.add_node(_parent)
                    _c_name = i.name if not _name_count else f'{i.name}{_name_count}'
                    _graph.add_edge(_parent, _c_name)
                    _node_dict[_c_name] = i
                _counter[i.name] += 1
                _traverse_html(i, _graph, _counter, i.name, _node_dict=_node_dict)
            except AttributeError:
                pass


def parse_tag(tag):
    return tag[:tag.find('')] if '' in tag else tag


def graph_builder(url):
    """fetch DOM elements from a URL and return a networkx graph as JSON"""
    # create an empty graph
    wg = nx.Graph()
    # get response from url
    response = requests.get(url, headers=HEADERS)
    # get soup
    soup = BeautifulSoup(response.content, "lxml")

    """Removes tags other than 'body' tag in html dom tree"""
    # remove garbage
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

    # create an empty node dictionary
    node_dict = {}
    # traverse through soup -> get graph
    _traverse_html(soup, wg, defaultdict(int), _node_dict=node_dict)
    # draw graph from networkx library
    nx.draw(wg, nx.planar_layout(wg), node_size = 20)
    return wg


def running():
    url_list = ["https://website1649510.nicepage.io/Contact.html?version=3e4b754f-560c-4f11-a59a-f4eccf6f5e53"] # Sampling
    graph_list = []
    for i in url_list:
        graph_list.append(graph_builder(i))


if __name__ == '__main__':
  running()

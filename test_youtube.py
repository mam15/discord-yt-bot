import os
from googleapiclient.errors import HttpError
import pytest
from youtube import YoutubeStream

@pytest.fixture
def obj():
    return YoutubeStream()

def test_search_noresult(obj):
    # Test query with no results
    with pytest.raises(ValueError):
        obj._search("trhjslkghfgmbndfghjoritpoeirtpaoweitpaweodfghsjghdfgjh") 
    
def test_search_invalidkey(obj):
    # Test invalid API key
    with pytest.raises(HttpError):
        obj.api_key = "1"
        obj.__init__()
        obj._search("Invalid API key")

def test_search_valid(obj):
    # Test valid API key and result
    assert type(obj._search("valid query")) is str

@pytest.mark.asyncio
async def test_stream(obj):
    result = await obj.stream("valid query")
    assert type(result) is tuple
    # remove file downloaded by stream
    if os.path.exists(result[1]):
        os.remove(result[1])

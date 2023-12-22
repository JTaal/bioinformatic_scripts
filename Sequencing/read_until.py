from concurrent.futures import ThreadPoolExecutor
import numpy
from read_until import ReadUntilClient

def analysis(client, *args, **kwargs):
    while client.is_running:
        for channel, read in client.get_read_chunks():
            raw_data = numpy.fromstring(read.raw_data, client.signal_dtype)
            # do something with raw data... and maybe call:
            #    client.stop_receiving_read(channel, read.number)
            #    client.unblock_read(channel, read.number)


ReadUntilClient.mk_host = 3306

read_until_client = ReadUntilClient()
read_until_client.run()
with ThreadPoolExecutor() as executor:
    executor.submit(analysis, read_until_client)
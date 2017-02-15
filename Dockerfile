FROM solr
RUN chgrp -R 0 /opt/solr \
  && RUN chmod -R g+rw /opt/solr \
  && RUN find /opt/solr -type d -exec chmod g+x {} +

FROM solr
RUN chgrp -R 0 /opt/solr \
  && chmod -R g+rwX /opt/solr 

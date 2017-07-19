FROM solr:latest

USER root

ADD nice2_index /opt/solr/server/solr/nice2_index
ADD nice2-enterprisesearch-impl-1.0-SNAPSHOT.jar /opt/solr/server/solr/lib
ADD tocco-solr.sh /usr/local/bin/

RUN chgrp -R 0 /opt/solr \
  && chmod -R g+rwX /opt/solr \
  && chmod +x /usr/local/bin/tocco-solr.sh

ENTRYPOINT ["tocco-solr.sh"]
CMD ["solr-foreground"]

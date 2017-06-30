FROM solr:latest

USER root

ADD nice2_index /opt/solr/server/solr/nice2_index
ADD nice2-enterprisesearch-impl-1.0-SNAPSHOT.jar /opt/solr/server/solr/lib

RUN chgrp -R 0 /opt/solr \
  && chmod -R g+rwX /opt/solr \

  # read section 'Timezone' in README.md for why this is needed
  && echo "Europe/Zurich" >/etc/timezone

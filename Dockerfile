FROM solr:latest

USER root

ADD conf /opt/solr/server/solr/mycores/
ADD nice2-enterprisesearch-impl-1.0-SNAPSHOT.jar /opt/solr/server/solr/lib

RUN chgrp -R 0 /opt/solr /opt/docker-solr \
  && chmod -R g+rwX /opt/solr /opt/docker-solr \

#  # read section 'Timezone' in README.md for why this is needed
#  && echo "Europe/Zurich" >/etc/timezone \

  # read section '.trashcan' in README.md for why this is needed
  && mkdir /persist \
  && chgrp 0 /persist/ \
  && chmod g+rwx /persist

CMD ["solr-create", "-c", "nice2_index"]

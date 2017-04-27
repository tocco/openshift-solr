FROM solr:latest

USER root
ADD nice2_index /opt/solr/server/solr/mycores/nice2_index
ADD nice2-enterprisesearch-impl-1.0-SNAPSHOT.jar /opt/solr/server/solr/lib
RUN chgrp -R 0 /opt/solr \
  && chmod -R g+rwX /opt/solr \

  # Solr fails to start if timezone on Gluster Cluster differ
  #
  # https://bugzilla.redhat.com/show_bug.cgi?id=1430659
  # https://discuss.elastic.co/t/es-cluster-in-docker-containers-alreadyclosedexception-underlying-file-changed-by-an-external-force/48874
  && echo "Europe/Zurich" >/etc/timezone

FROM cielavenir/openrave:jammy

ARG DEBIAN_FRONTEND="noninteractive"
ARG YCM="0.15.3"
ARG YARP="3.7.2"
ARG OPENRAVE_YARP_PLUGINS_COMMIT="72a5a0cedd644d11b535e7a406f7f2ba4990171a"
ARG TEO_OPENRAVE_MODELS="0.1.0"
ARG TEO_CONFIGURATION_FILES_COMMIT="69228d5d6706eaa2d9a6ca81d380577bb5dc9ae0"
ARG TOOLS_COMMIT="cc18a5f47ff26809f83f35485712ea6d86afb460"
ARG OROCOS_KINEMATICS_DYNAMICS="1.5.1"
ARG KINEMATICS_DYNAMICS_COMMIT="f4bc01f1325efc64317be58e4eeb3fc44f27f496"

RUN apt update \
    && apt install -y --no-install-recommends \
        wget swig \
        qtbase5-dev qtdeclarative5-dev qtmultimedia5-dev qml-module-qtquick2 qml-module-qtquick-window2 qml-module-qtmultimedia \
        qml-module-qtquick-dialogs qml-module-qtquick-controls qml-module-qt-labs-folderlistmodel qml-module-qt-labs-settings \
        libedit-dev \
    \
    && wget -q https://github.com/robotology/ycm/archive/refs/tags/v$YCM.tar.gz \
    && tar -xzf v$YCM.tar.gz \
    && mkdir -p ycm-$YCM/build && cd ycm-$YCM/build && cmake .. \
    && make -j$(nproc) && make install && cd ../.. && rm v$YCM.tar.gz \
    \
    && wget -q https://github.com/robotology/yarp/archive/refs/tags/v$YARP.tar.gz \
    && tar -xzf v$YARP.tar.gz \
    && mkdir -p yarp-$YARP/build && cd yarp-$YARP/build \
    && cmake .. -DSKIP_ACE=ON \
        -DCREATE_GUIS=ON -DENABLE_yarpcar_mjpeg=ON -DENABLE_yarppm_depthimage_to_mono=ON -DENABLE_yarppm_depthimage_to_rgb=ON \
        -DYARP_COMPILE_BINDINGS=ON -DCREATE_PYTHON=ON -DCMAKE_INSTALL_PYTHON3DIR=/usr/local/lib/python3.10/dist-packages \
    && make -j$(nproc) && make install && cd ../.. && rm v$YARP.tar.gz \
    \
    && wget -q https://github.com/roboticslab-uc3m/openrave-yarp-plugins/archive/$OPENRAVE_YARP_PLUGINS_COMMIT.tar.gz \
    && tar -xzf $OPENRAVE_YARP_PLUGINS_COMMIT.tar.gz \
    && mkdir -p openrave-yarp-plugins-$OPENRAVE_YARP_PLUGINS_COMMIT/build && cd openrave-yarp-plugins-$OPENRAVE_YARP_PLUGINS_COMMIT/build && cmake .. \
    && make -j$(nproc) && make install && cd ../.. && rm $OPENRAVE_YARP_PLUGINS_COMMIT.tar.gz \
    \
    && wget -q https://github.com/roboticslab-uc3m/teo-openrave-models/archive/refs/tags/v$TEO_OPENRAVE_MODELS.tar.gz \
    && tar -xzf v$TEO_OPENRAVE_MODELS.tar.gz \
    && mkdir -p teo-openrave-models-$TEO_OPENRAVE_MODELS/build && cd teo-openrave-models-$TEO_OPENRAVE_MODELS/build && cmake .. \
    && make -j$(nproc) && make install && cd ../.. && rm v$TEO_OPENRAVE_MODELS.tar.gz \
    \
    && wget -q https://github.com/roboticslab-uc3m/teo-configuration-files/archive/$TEO_CONFIGURATION_FILES_COMMIT.tar.gz \
    && tar -xzf $TEO_CONFIGURATION_FILES_COMMIT.tar.gz \
    && mkdir -p teo-configuration-files-$TEO_CONFIGURATION_FILES_COMMIT/build && cd teo-configuration-files-$TEO_CONFIGURATION_FILES_COMMIT/build && cmake .. \
    && make -j$(nproc) && make install && cd ../.. && rm $TEO_CONFIGURATION_FILES_COMMIT.tar.gz \
    \
    && wget -q https://github.com/roboticslab-uc3m/tools/archive/$TOOLS_COMMIT.tar.gz \
    && tar -xzf $TOOLS_COMMIT.tar.gz \
    && mkdir -p tools-$TOOLS_COMMIT/build && cd tools-$TOOLS_COMMIT/build && cmake .. \
    && make -j$(nproc) && make install && cd ../.. && rm $TOOLS_COMMIT.tar.gz \
    \
    && wget -q https://github.com/orocos/orocos_kinematics_dynamics/archive/refs/tags/v$OROCOS_KINEMATICS_DYNAMICS.tar.gz \
    && tar -xzf v$OROCOS_KINEMATICS_DYNAMICS.tar.gz \
    && mkdir -p orocos_kinematics_dynamics-$OROCOS_KINEMATICS_DYNAMICS/orocos_kdl/build && cd orocos_kinematics_dynamics-$OROCOS_KINEMATICS_DYNAMICS/orocos_kdl/build && cmake .. \
    && make -j$(nproc) && make install && cd ../../.. && rm v$OROCOS_KINEMATICS_DYNAMICS.tar.gz \
    \
    && wget -q https://github.com/roboticslab-uc3m/kinematics-dynamics/archive/$KINEMATICS_DYNAMICS_COMMIT.tar.gz \
    && tar -xzf $KINEMATICS_DYNAMICS_COMMIT.tar.gz \
    && mkdir -p kinematics-dynamics-$KINEMATICS_DYNAMICS_COMMIT/build && cd kinematics-dynamics-$KINEMATICS_DYNAMICS_COMMIT/build \
    && cmake .. -DCREATE_PYTHON=ON -DCREATE_BINDINGS_PYTHON=ON -DCMAKE_INSTALL_PYTHONDIR=/usr/local/lib/python3.10/dist-packages \
    && make -j$(nproc) && make install && cd ../.. && rm $KINEMATICS_DYNAMICS_COMMIT.tar.gz \
    \
    && ldconfig

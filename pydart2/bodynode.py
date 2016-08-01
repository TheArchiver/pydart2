# Copyright (c) 2015, Disney Research
# All rights reserved.
#
# Author(s): Sehoon Ha <sehoon.ha@disneyresearch.com>
# Disney Research Robotics Group
import pydart2_api as papi
import numpy as np


class BodyNode(object):
    def __init__(self, _skel, _id):
        self.skel = _skel
        self._id = _id
        self.name = papi.bodynode__getName(self.wid, self.skid, self.id)
        self.parent_bodynode = None
        self.child_bodynodes = list()

        self.parent_joint = None
        self.child_joints = list()

        self.dependent_dofs = list()
        self.markers = list()  # Built by markers

    def build(self):
        # Build Body Nodes
        self.parent_bodynode = None
        self.child_bodynodes = list()

        ret_id = papi.bodynode__getParentBodyNode(self.wid, self.skid, self.id)
        if ret_id >= 0:
            self.parent_bodynode = self.skel.bodynodes[ret_id]

        num = papi.bodynode__getNumChildBodyNodes(self.wid, self.skid, self.id)
        for index in range(num):
            ret_id = papi.bodynode__getChildBodyNode(self.wid,
                                                     self.skid,
                                                     self.id,
                                                     index)
            if ret_id >= 0:
                self.child_bodynodes.append(self.skel.bodynodes[ret_id])

        # Build Joints
        self.parent_joint = None
        self.child_joints = list()
        ret_id = papi.bodynode__getParentJoint(self.wid, self.skid, self.id)
        if ret_id >= 0:
            self.parent_joint = self.skel.joints[ret_id]

        num = papi.bodynode__getNumChildJoints(self.wid, self.skid, self.id)
        for index in range(num):
            ret_id = papi.bodynode__getChildJoint(self.wid,
                                                  self.skid,
                                                  self.id,
                                                  index)
            if ret_id >= 0:
                self.child_joints.append(self.skel.joints[ret_id])

        # Build dependent_dofs
        self.dependent_dofs = list()
        num = papi.bodynode__getNumDependentDofs(self.wid, self.skid, self.id)
        for index in range(num):
            ret_id = papi.bodynode__getDependentDof(self.wid,
                                                    self.skid,
                                                    self.id,
                                                    index)
            if ret_id >= 0:
                self.dependent_dofs.append(self.skel.dofs[ret_id])

        # Build markers (by other class)
        self.markers = list()

    def num_child_bodynodes(self, ):
        return len(self.child_bodynodes)

    def num_dependent_dofs(self, ):
        return len(self.dependent_dofs)

    def num_child_joints(self, ):
        return len(self.child_joints)

    def num_markers(self, ):
        return len(self.markers)

    @property
    def id(self):
        return self._id

    @property
    def wid(self):
        return self.skel.world.id

    @property
    def skid(self):
        return self.skel.id

    # def num_contacts(self):
    #     return papi.getBodyNodeNumContacts(self.wid, self.skid, self.id)

    # def contacts(self):
    #     n = self.num_contacts()
    #     contacts = papi.getBodyNodeContacts(self.wid,
    #                                         self.skid,
    #                                         self.id, 7 * n)
    #     return [Contact(contacts[7 * i: 7 * (i + 1)]) for i in range(n)]

########################################
# Index Functions
    def index_in_skeleton(self, ):
        return papi.bodynode__getIndexInSkeleton(self.wid, self.skid, self.id)

    def index_in_tree(self, ):
        return papi.bodynode__getIndexInTree(self.wid, self.skid, self.id)

    def tree_index(self, ):
        return papi.bodynode__getTreeIndex(self.wid, self.skid, self.id)

########################################
# Property Functions
    def set_gravity_mode(self, _gravityMode):
        papi.bodynode__setGravityMode(self.wid,
                                      self.skid,
                                      self.id,
                                      _gravityMode)

    def gravity_mode(self, ):
        return papi.bodynode__getGravityMode(self.wid, self.skid, self.id)

    def is_collidable(self, ):
        return papi.bodynode__isCollidable(self.wid, self.skid, self.id)

    def set_collidable(self, _isCollidable):
        papi.bodynode__setCollidable(self.wid,
                                     self.skid,
                                     self.id,
                                     _isCollidable)

########################################
# Inertia Functions
    def mass(self):
        return papi.bodynode__getMass(self.wid, self.skid, self.id)

    @property
    def m(self):
        return self.mass()

    def inertia(self):
        return papi.bodynode__getInertia(self.wid, self.skid, self.id)

    @property
    def I(self):
        return self.inertia()

########################################
# Momentum Functions
    def local_com(self, ):
        return papi.bodynode__getLocalCOM(self.wid, self.skid, self.id)

    def com(self, ):
        return papi.bodynode__getCOM(self.wid, self.skid, self.id)

    @property
    def C(self):
        return self.com()

    def com_linear_velocity(self, ):
        return papi.bodynode__getCOMLinearVelocity(self.wid,
                                                   self.skid,
                                                   self.id)

    @property
    def dC(self):
        return self.com_linear_velocity()

    def com_spatial_velocity(self, ):
        return papi.bodynode__getCOMSpatialVelocity(self.wid,
                                                    self.skid,
                                                    self.id)

    def com_linear_acceleration(self, ):
        return papi.bodynode__getCOMLinearAcceleration(self.wid,
                                                       self.skid,
                                                       self.id)

    def com_spatial_acceleration(self, ):
        return papi.bodynode__getCOMSpatialAcceleration(self.wid,
                                                        self.skid,
                                                        self.id)

########################################
# Friction and Restitution Functions
    def set_friction_coeff(self, _coeff):
        papi.bodynode__setFrictionCoeff(self.wid, self.skid, self.id, _coeff)

    def friction_coeff(self, ):
        return papi.bodynode__getFrictionCoeff(self.wid, self.skid, self.id)

    def set_restitution_coeff(self, _coeff):
        papi.bodynode__setRestitutionCoeff(self.wid,
                                           self.skid,
                                           self.id,
                                           _coeff)

    def restitution_coeff(self, ):
        return papi.bodynode__getRestitutionCoeff(self.wid, self.skid, self.id)

########################################
# Transform Functions
    def transform(self, ):
        return papi.bodynode__getTransform(self.wid, self.skid, self.id)

    @property
    def T(self):
        return self.transform()

    def to_world(self, x):
        x_ = np.append(x, [1.0])
        return (self.T.dot(x_))[:3]

    def to_local(self, x):
        Tinv = np.linalg.inv(self.T)
        x_ = np.append(x, [1.0])
        return (Tinv.dot(x_))[:3]

    def world_transform(self, ):
        return papi.bodynode__getWorldTransform(self.wid, self.skid, self.id)

    def relative_transform(self, ):
        return papi.bodynode__getRelativeTransform(self.wid,
                                                   self.skid,
                                                   self.id)

    # def bounding_box_dims(self):
    #     return papi.getBodyNodeShapeBoundingBoxDim(self.wid,
    #                                                self.skid,
    #                                                self.id)
    # def world_linear_jacobian(self, offset=None):
    #     if offset is None:
    #         offset = np.zeros(3)
    #     J = np.zeros((3, self.skel.ndofs))
    #     papi.getBodyNodeWorldLinearJacobian(self.wid, self.skid,
    #                                         self.id, offset, J)
    #     return J

    # @property
    # def J(self, offset=None):
    #     return self.world_linear_jacobian(offset)

    def add_ext_force(self,
                      _force,
                      _offset=None,
                      _isForceLocal=False,
                      _isOffsetLocal=True):
        if _offset is None:
            _offset = np.zeros(3)
        papi.bodynode__addExtForce(self.wid,
                                   self.skid,
                                   self.id,
                                   _force,
                                   _offset,
                                   _isForceLocal,
                                   _isOffsetLocal)

    def set_ext_force(self,
                      _force,
                      _offset=None,
                      _isForceLocal=False,
                      _isOffsetLocal=True):
        if _offset is None:
            _offset = np.zeros(3)
        papi.bodynode__setExtForce(self.wid,
                                   self.skid,
                                   self.id,
                                   _force,
                                   _offset,
                                   _isForceLocal,
                                   _isOffsetLocal)

    def add_ext_torque(self, _torque, _isLocal=False):
        papi.bodynode__addExtTorque(self.wid, self.skid, self.id,
                                    _torque, _isLocal)

    def set_ext_torque(self, _torque, _isLocal=False):
        papi.bodynode__setExtTorque(self.wid, self.skid, self.id,
                                    _torque, _isLocal)

    # def num_markers(self):
    #     return papi.getBodyNodeNumMarkers(self.wid, self.skid, self.id)

    # def get_marker_local_pos(self, mid):
    #     return papi.getMarkerLocalPosition(self.wid, self.skid, self.id, mid)

    # def get_marker_pos(self, mid):
    #     return papi.getMarkerPosition(self.wid, self.skid, self.id, mid)

    def __repr__(self):
        return '[BodyNode(%d): %s]' % (self.id, self.name)

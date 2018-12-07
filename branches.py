"""
Module that provides the API for the branches
"""
# from config import db
from models import Branch, BranchSchema


def read_all():
    """
    Responds to a request for /api/branches with the complete list of
    branches, sorted by branch number
    """
    # Create the list of branches
    branches = Branch.query.order_by(Branch.number).all()

    # Serialize the data for the response
    branch_schema = BranchSchema(many=True)
    return branch_schema.dump(branches).data


def read_one(number):
    """
    Responds to a request for /api/branches/{number} with one matching branch
    from branches

    :param number:   DMV designated number of the branch to find
    :return:         branch matching number
    """
    # Get the requested branch
    branch = Branch.query.filter(Branch.number == number).one_or_none()

    # Did we find the branch?
    if branch is not None:
        # Serialize the data for the response
        branch_schema = BranchSchema()
        return branch_schema.dump(branch).data
    
    # Otherwise, nope, didn't find the branch
    else:
        # abort(404, f'Branch not found for number: {number}')
        pass


def read_region(region):
    """
    Responds to a request for /api/branches/region/{region} with one matching branch from branches

    :param number:   DMV region number of the branch to find
    :return:         branch matching region
    """
    # Get the requested region
    branches = Branch.query.filter(Branch.region == region).all()
    # print(f'There are {branches.count()} branches in region {region}')

    # Did we find the regoin?
    if branches:
        # Serialize the data for the response
        branch_schema = BranchSchema(many=True)
        return branch_schema.dump(branches).data

    # Otherwise, nope, didn't find the branch
    else:
        # abort(404, f'Branch not found for region: {region}')
        pass

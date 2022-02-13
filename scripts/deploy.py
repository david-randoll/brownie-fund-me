from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # if we are on the persistent network like Rinkeby, use the associated address
        pricefeed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # otherwise, deploy mock pricefeed
        deploy_mocks()
        pricefeed_address = MockV3Aggregator[-1].address

    # pass the pricefeed address to the FundMe contract constructor
    fund_me = FundMe.deploy(
        pricefeed_address,
        {"from": get_account()},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"FundMe contract deployed at {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

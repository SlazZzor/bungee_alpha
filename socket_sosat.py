from web3 import Web3
from time import sleep
from random import randint, shuffle
from os import system, name
from config import *
import json


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def input_data():
    from_network = 0
    to = 0
    amount = 0
    try:
        while from_network <= 0 or to <= 0 or from_network >= 6 or to >= 6 or from_network == to:
            from_network  = int(input('\n--------------------\nEthereum - 1\nArbitrum - 2\nOptimism - 3\nMatic - 4\nBSC - 5\nВведите номер сети откуда отправлять\n--------------------\n'))
            clear()
            to = int(input('\n--------------------\nEthereum - 1\nArbitrum - 2\nOptimism - 3\nMatic - 4\nBSC - 5\nВведите номер сети куда отправлять\n--------------------\n'))
            clear()

        from_network = network[from_network - 1]
        to = network[to - 1]
        min = transfer_limit[from_network][to]['min']
        max = transfer_limit[from_network][to]['max']
        ticker = currency[from_network]

        while amount <= 0:
            print('Минимальная стоимость транзакции:', min, ticker, '\nМаксимальная стоимость транзакции:', max, ticker, '\n')
            print('WARNING: на самом деле нет никаких ограничений по минимальной транзакции, я убрал все ограничения, но ставя ниже минимума вы действуете на свой страх и риск! (как и впринципе просто взаимодействуя со скриптом)')
            amount = float(input('Введите количество в ' + ticker + ' которое вы будете отправлять на каждом аккаунте\nПример: 0.02\n'))
            clear()
    except:
        clear()
        print('Ошибка. Повторите ещё раз и проверьте введёную информацию')
        return input_data()
    return from_network, to, amount


def send_trx(wallet, i):
    try:
        wallet = wallet.replace('\n', '')
        account = web3.eth.account.from_key(wallet)
        transaction = contract.functions.depositNativeToken(network_chain_id[to], account.address).build_transaction({
            'value': web3.to_wei(amount, 'ether'),
            'chainId': providers[from_network]['chainId'],
            'gas': gas_limit[from_network],
            'gasPrice': gas,
            'nonce': web3.eth.get_transaction_count(account.address),
        })
        signed_tx = web3.eth.account.sign_transaction(transaction, account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash
    except Exception as error:
        if "insufficient funds for gas * price + value" in str(error):
            print('На', i, 'кошельке не хватает баланса для транзакции\nЛог ошибки:', str(error))
        elif 'intrinsic gas too low' in str(error):
            print('Недостаточно gas limit для транзакции\nЛог ошибки:', str(error))
        else:
            print('Что-то пошло не так на кошельке под номером:', index, 'ошибка:', error)
        return 0
    
    


    

ERC20_ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"destinationReceiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"destinationChainId","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Donation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"GrantSender","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"RevokeSender","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"srcChainTxHash","type":"bytes32"}],"name":"Send","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[{"components":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"internalType":"struct GasMovr.ChainData[]","name":"_routes","type":"tuple[]"}],"name":"addRoutes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable[]","name":"receivers","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes32[]","name":"srcChainTxHashes","type":"bytes32[]"},{"internalType":"uint256","name":"perUserGasAmount","type":"uint256"},{"internalType":"uint256","name":"maxLimit","type":"uint256"}],"name":"batchSendNativeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"chainConfig","outputs":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"depositNativeToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"getChainData","outputs":[{"components":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"internalType":"struct GasMovr.ChainData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"grantSenderRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"processedHashes","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"revokeSenderRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"receiver","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainTxHash","type":"bytes32"},{"internalType":"uint256","name":"perUserGasAmount","type":"uint256"},{"internalType":"uint256","name":"maxLimit","type":"uint256"}],"name":"sendNativeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"senders","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"_isEnabled","type":"bool"}],"name":"setIsEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setPause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setUnPause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"withdrawFullBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')

providers = {
    'matic': {'chainId': 137,
              "rpc": 'https://polygon.llamarpc.com',
              "name": 'matic'},
    'bsc': {'chainId': 56,
            "rpc": 'https://bsc-dataseed.binance.org/',
            "name": 'bsc'},
    'ethereum': {'chainId': 1,
            "rpc": 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
            "name": 'ethereum'},
    'optimism': {'chainId': 10,
            "rpc": 'https://mainnet.optimism.io',
            "name": 'optimism'},
    'arbitrum': {'chainId': 42161,
                "rpc": 'https://arb1.arbitrum.io/rpc',
                "name": 'arbitrum'},
}


gas_limit = {   
    'ethereum': 21000,
    'arbitrum': 3000000,
    'optimism': 50000,
    'matic': 100000,
    'bsc': 100000,
}

network_chain_id = {
    'ethereum' : 1,
    'arbitrum': 42161,
    'optimism': 10,
    'matic': 137,
    'bsc': 56,
}

currency = {   
    'ethereum': 'ETH',
    'arbitrum': 'ETH',
    'optimism': 'ETH',
    'matic': 'MATIC',
    'bsc': 'BNB',
}

contracts = {
    'ethereum': '0xb584D4bE1A5470CA1a8778E9B86c81e165204599',
    'arbitrum': '0xc0E02AA55d10e38855e13B64A8E1387A04681A00',
    'optimism': '0x5800249621DA520aDFdCa16da20d8A5Fc0f814d8',
    'matic': '0xAC313d7491910516E06FBfC2A0b5BB49bb072D91',
    'bsc': '0xBE51D38547992293c89CC589105784ab60b004A9',
}

transfer_limit = {
    'ethereum': {
        'arbitrum': {
            'min': 0.003,
            'max': 0.034
        },
        'optimism': {
            'min': 0.0034,
            'max': 0.034
        },
        'matic': {
            'min': 0.00018,
            'max': 0.015
        },
        'bsc': {
            'min': 0.005,
            'max': 0.0012
                },
    },
    'arbitrum': {
        'matic': {
            'min': 0.00018,
            'max': 0.015
        },
        'optimism': {
            'min': 0.0034,
            'max': 0.034
        },
        'ethereum': {
            'min': 0.005,
            'max': 10,
            'restricted': True
        },
        'bsc': {
            'min': 0.00023,
            'max': 0.0012
        },
    },

    'optimism': {
        'matic': {
            'min': 0.00018, 
            'max': 0.015
        },
        'arbitrum': {
            'min': 0.0028,
            'max': 0.034
        },
        'ethereum': {
            'min': 0.005,
            'max': 10,
            'restricted': True,
        },
        'bsc': {
            'min': 0.00023,
            'max': 0.0012
        },
    },
    'matic': {
        'optimism': {
            'min': 6.28,
            'max': 66.43    
        },
        'arbitrum': {            
            'min': 5.28,
            'max': 66.43
        },
        'ethereum': {
            'min': 0.005,
            'max': 10,
        'restricted': True
        },
        'bsc': {
            'min': 0.43,
            'max': 2.53
        },
        },
    'bsc': {
        'optimism': {
            'min': 0.022,
            'max': 0.2
        },
        'arbitrum': {
            'min': 0.017,
            'max': 0.2
        },
        'ethereum': {
            'min': 0.005,
            'max': 10,
            'restricted': True
        },
        'matic': {
            'min': 0.0011,
            'max': 0.092
        },
    },
}


network = ['ethereum', 'arbitrum', 'optimism', 'matic', 'bsc']




from_network, to, amount = input_data()

web3 = Web3(Web3.HTTPProvider(providers[from_network]['rpc']))
web3.eth.account.enable_unaudited_hdwallet_features()
contract = web3.eth.contract(address = contracts[from_network], abi = ERC20_ABI )
gas =  web3.eth.gas_price

failed_wallets = []

clear()
print ('Вы отправляете из сети', from_network, 'в сеть', to, amount, currency[from_network],'\nТранзакция придёт в нативной валюте сети в которую вы отправляете\n')


print('Пожалуйста, проверьте чтобы на всех ваших аккаунтов был достаточный баланс для отправки и оплаты комиссии!\nВведите Y чтобы начать или что-угодно другое чтобы отменить')
if str(input()).lower() == 'y':
    clear()
    with open('private_keys.txt', 'r') as file:
        wallets = file.readlines()
        wallets_sample = wallets.copy()
        if randomize:
            shuffle(wallets)
        for wallet in wallets:
            index = wallets_sample.index(wallet) + 1
            tx_hash = send_trx(wallet, index)

            if tx_hash != 0:
                print('Успешно провёл транзакцию. Номер кошелька:', index, '. Хэш транзакции:', web3.to_hex(tx_hash))
            else:
                failed_wallets.append(wallet)

            sleep(delay)
else:
    print('Отменено.')
    

if failed_wallets:
    with open('failed_private_keys.txt', 'w') as file:
        for wallet in failed_wallets:
            file.write(wallet)
    print('Все приватники кошельков на которых провалились транзакции были занесены в файл failed_private_keys.txt')

from aptos_sdk.account import Account
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# 文件名
output_full_info = 'aptos_miye.txt'  # 保存完整信息的文件
output_addr_info = 'aptos_addr.txt'  # 保存序号和地址的文件

mnemo = Mnemonic("english")

def generate_wallets(n):
    # 打开两个文件，准备写入信息
    with open(output_full_info, 'w') as f_full, open(output_addr_info, 'w') as f_addr:
        # 写入文件标题
        f_full.write("序号, 地址, 助记词, 私钥\n")
        f_addr.write("序号, 地址\n")
        
        # 循环生成 n 个钱包
        for i in range(1, n + 1):
            # 使用 Mnemonic 生成12个单词的助记词
            mnemonic = mnemo.generate(strength=128)

            # 生成种子
            seed = Mnemonic.to_seed(mnemonic)

            # 使用BIP44标准生成私钥，Aptos使用的是m/44'/637'/0'/0/0路径
            bip44_mst = Bip44.FromSeed(seed, Bip44Coins.APTOS)
            bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

            # 获取钱包的地址和私钥
            account = Account.load_key(bip44_acc.PrivateKey().Raw().ToHex())
            address = account.address()
            private_key = account.private_key.hex()

            # 输出信息到控制台，并确保同一行显示
            print(f"{i}, {address}, {mnemonic}, {private_key}")
            
            # 写入完整信息到 aptos_miye.txt 文件
            f_full.write(f"{i}, {address}, {mnemonic}, {private_key}\n")
            
            # 写入序号和地址到 aptos_addr.txt 文件
            f_addr.write(f"{i}, {address}\n")
    
    print(f"完整信息已保存到 {output_full_info}")
    print(f"序号和地址已保存到 {output_addr_info}")

if __name__ == "__main__":
    num_wallets = int(input("请输入要生成的钱包数量: "))
    generate_wallets(num_wallets)

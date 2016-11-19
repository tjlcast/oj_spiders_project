# -*- coding:utf-8 -*-

# private protected public

test_info = {
'4'  :[  {
        'user_name': 'huanghai',
        'pro_info': [
            {
                "prob_title": 'switch结构练习',
                "prob_priv": 'protected',
                'prob_desc': """
输入一个考试结果,90分以上输出A,80以上输出B,以此类推；60以下输出E.

程序运行效果：
Sample 1:
10↙
E
Sample 2:
100↙
A

                            """,
                'prob_input_desc': """
输入一个整数n(1<=n<=100)
                                    """,
                'prob_output_desc': """
输出对应的考试结果
                                    """,
                'prob_input_sample': '见题目描述',
                'prob_output_sample': '见题目描述',
                'files_num': 2,
            },
            {
                "prob_title": '数列求和',
                "prob_priv": 'protected',
                'prob_desc': """
有一分数序列：2/1, 3/2, 5/3, 8/5, 13/8, 21/13,……,先观察数列规律，再求出这个数列的前n项之和。考虑到提高结果精度，请用double型变量存储结果。

程序运行效果：

Sample 1:
10↙
16.48
Sample 2:
25↙
40.75

                            """,
                'prob_input_desc': """
输入一个正整数n(1<=n<=50)，代表数列的项数。
                                    """,
                'prob_output_desc': """
输出序列的前n项和。

                                    """,
                'prob_input_sample': '见题目描述',
                'prob_output_sample': '见题目描述',
                'files_num': 2,
            },
{
                "prob_title": '千分位格式',
                "prob_priv": 'protected',
                'prob_desc': """
已知一个正整数n，你要将它输出成“千分位”形式。即从个位数起，每3位之间加一个逗号。例如，将“7654321”写成“7,654,321”。


程序运行效果：

Sample 1:
6324112↙
6,324,112
Sample 2:
45634523↙
45,634,523

                            """,
                'prob_input_desc': """
输入一个正整数n。
                                    """,
                'prob_output_desc': """
输出这个整数的“千分位”输出形式，占一行。

                                    """,
                'prob_input_sample': '见题目描述',
                'prob_output_sample': '见题目描述',
                'files_num': 2,
            },
{
                "prob_title": '设计函数GCD与LCM',
                "prob_priv": 'protected',
                'prob_desc': """
设计函数int GCD(int a,int b)和int LCM(int a,int b)，分别用于求正整数a和b的最大公约数和最小公倍数。如GCD(32,48)为16，LCM(32,48)为96。


程序运行效果：

Sample 1:
13 7↙
1 91


                            """,
                'prob_input_desc': """
输入两个个正整数n和m（空格分隔）。
                                    """,
                'prob_output_desc': """
输出n和m的最大公约数和最小公倍数（空格分隔）。
                                    """,
                'prob_input_sample': '见题目描述',
                'prob_output_sample': '见题目描述',
                'files_num': 2,
            },
        ],

    }
    ]
}


if __name__ == '__main__':
    pass

import numpy as np
import matplotlib.pyplot as plt


def make_plot():
    label = 'pt_like'
    label = '.'


    num_shots = np.load(label + '/num_shots.npy')
    res_1 = np.load(label + '/res_1.npy')
    res_2 = np.load(label + '/res_2.npy')
    res_3 = np.load(label + '/res_3.npy')
    res_4 = np.load(label + '/res_4.npy')
    res_1_n = np.load(label + '/res_1_n.npy')
    res_2_n = np.load(label + '/res_2_n.npy')
    res_3_n = np.load(label + '/res_3_n.npy')
    res_4_n = np.load(label + '/res_4_n.npy')


    fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(4, 5))

    axs[0].plot(num_shots, res_1, '.g-')
    axs[0].text(num_shots[-2], res_1[-1], 'sample1', color='g', fontsize=12)
    axs[0].plot(num_shots, res_2, '.-', color='red')
    axs[0].text(num_shots[-2], res_2[-1], 'sample2', color='red', fontsize=12)
    axs[0].plot(num_shots, res_3, '.-', color='tomato')
    axs[0].text(num_shots[-2], res_3[-1], 'sample3', color='tomato', fontsize=12)
    # axs[0].plot(num_shots, res_4, '.-', color='salmon')
    # axs[0].text(num_shots[-2], res_4[-1], 'sample4', color='salmon', fontsize=12)
    axs[0].plot(num_shots, res_4, '.-', color='limegreen')
    axs[0].text(num_shots[-2], res_4[-1], 'sample4', color='limegreen', fontsize=12)

    axs[0].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[0].set_xscale('log')
    # axs[0, 0].set_yscale('log')
    # axs[0, 0].set_xlabel('Num. shots', fontsize=12)
    axs[0].set_ylabel('Probability', fontsize=12)
    axs[0].set_title(r'Fidelity  $F(\rho_{B_n}, \rho_{expected})$')
    axs[0].set_title(r'Fidelity  $F(C_{B_n}, C_{expected})$')
    axs[0].tick_params(direction="in")

    axs[1].plot(num_shots, res_1_n, '.g-')
    axs[1].text(num_shots[-2], res_1_n[-1], 'sample1', color='g', fontsize=12)
    axs[1].plot(num_shots, res_2_n,  '.-', color='red')
    axs[1].text(num_shots[-2], res_2_n[-1], 'sample2', color='red', fontsize=12)
    axs[1].plot(num_shots, res_3_n,  '.-', color='tomato')
    axs[1].text(num_shots[-2], res_3_n[-1], 'sample3', color='tomato', fontsize=12)
    # axs[1].plot(num_shots, res_4_n,  '.-', color='salmon')
    # axs[1].text(num_shots[-2], res_4_n[-1], 'sample4', color='salmon', fontsize=12)
    axs[1].plot(num_shots, res_4_n,  '.-', color='limegreen')
    axs[1].text(num_shots[-2], res_4_n[-1], 'sample4', color='limegreen', fontsize=12)

    axs[1].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[1].set_xscale('log')
    axs[1].set_xlabel('Num. shots', fontsize=12)
    axs[1].set_ylabel('Probability', fontsize=12)
    axs[1].tick_params(direction="in")

    plt.tight_layout()
    plt.show()


def plot(num_shots, res, res_n, col, style, title, title1):


    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(8, 3))

    for j, item in enumerate(res):
        axs[0].plot(num_shots, item, style[j], color=col[j])
        axs[0].text(num_shots[-2], item[-1], title[j], color=col[j], fontsize=12)

    axs[0].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')
    axs[0].set_xscale('log')
    # axs[0, 0].set_yscale('log')
    # axs[0, 0].set_xlabel('Num. shots', fontsize=12)
    axs[0].set_ylabel('Probability', fontsize=12)
    axs[0].set_xlabel('Num. shots', fontsize=12)
    axs[0].set_title(title1)
    axs[0].tick_params(direction="in")

    for j, item in enumerate(res_n):

        axs[1].plot(num_shots, item, style[j], color=col[j])
        axs[1].text(num_shots[-2], item[-1], title[j], color=col[j], fontsize=12)

    axs[1].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[1].set_xscale('log')
    axs[1].set_xlabel('Num. shots', fontsize=12)
    # axs[1].set_ylabel('Probability', fontsize=12)
    axs[1].set_title(title1)
    axs[1].tick_params(direction="in")

    plt.tight_layout()
    plt.show()

def make_plot1():

    num_shots = np.load('num_shots.npy')
    fidelity_noiseless = np.load('fidelity_noiseless.npy')
    fidelity_noisy = np.load('fidelity_noisy.npy')

    fidelity_noiseless1 = fidelity_noiseless[:, :4].T
    fidelity_noisy1 = fidelity_noisy[:, :4].T

    fidelity_noiseless2 = fidelity_noiseless[:, 4:].T
    fidelity_noisy2 = fidelity_noisy[:, 4:].T


    col = ['g', 'red', 'tomato', 'limegreen']
    style = ['.-', '.-', '.-', '.-']
    title = ['sample1', 'sample2', 'sample3', 'sample4']

    plot(num_shots, fidelity_noiseless1, fidelity_noisy1, col, style, title, r'Fidelity  $F(\rho_{B_n}, \rho_{expected})$')

    col = ['g', 'red', 'tomato', 'salmon']

    plot(num_shots, fidelity_noiseless2, fidelity_noisy2, col, style, title, r'Fidelity  $F(C_{B_n}, C_{expected})$')


def make_plot2():

    num_shots = np.load('shots_rng.npy')
    fid_noiseless = np.load('fidelity_noiseless_rng.npy')
    fid_noisy = np.load('fidelity_noisy_rng.npy')

    time_noiseless = np.load('time_noiseless_rng.npy')
    time_noisy = np.load('time_noisy_rng.npy')

    plt.plot(time_noiseless[:, 0] / num_shots)
    plt.plot(time_noiseless[:, 1] / num_shots)
    plt.plot(time_noiseless[:, 2] / num_shots)
    plt.plot(time_noiseless[:, 3] / num_shots)
    plt.plot(time_noiseless[:, 4] / num_shots)
    plt.plot(time_noiseless[:, 5] / num_shots)
    plt.yscale('log')
    plt.show()

    plt.plot(time_noisy[:, 0] / num_shots)
    plt.plot(time_noisy[:, 1] / num_shots)
    plt.plot(time_noisy[:, 2] / num_shots)
    plt.plot(time_noisy[:, 3] / num_shots)
    plt.plot(time_noisy[:, 4] / num_shots)
    plt.plot(time_noisy[:, 5] / num_shots)
    plt.yscale('log')
    plt.show()

    print(time_noiseless[-1, 0] / num_shots[-1])
    print(time_noiseless[-1, 1] / num_shots[-1])
    print(time_noiseless[-1, 2] / num_shots[-1])
    print(time_noiseless[-1, 3] / num_shots[-1])
    print(time_noiseless[-1, 4] / num_shots[-1])
    print(time_noiseless[-1, 5] / num_shots[-1])

    print(time_noisy[-1, 0] / num_shots[-1])
    print(time_noisy[-1, 1] / num_shots[-1])
    print(time_noisy[-1, 2] / num_shots[-1])
    print(time_noisy[-1, 3] / num_shots[-1])
    print(time_noisy[-1, 4] / num_shots[-1])
    print(time_noisy[-1, 5] / num_shots[-1])

    col = ['g', 'red', 'tomato', 'limegreen']
    style = ['.-', '.-', '.-', '.-']
    title = ['sample1', 'sample2', 'sample3', 'sample4']

    fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(12, 5))

    axs[0, 0].plot(num_shots, fid_noiseless[:, 0], style[0], color=col[0])
    axs[0, 0].text(num_shots[-2], fid_noiseless[:, 0][-1] - 0.1, title[0], color=col[0], fontsize=12)
    axs[0, 0].plot(num_shots, fid_noiseless[:, 1], style[1], color=col[1])
    axs[0, 0].text(num_shots[-2], fid_noiseless[:, 1][-1] + 0.05, title[1], color=col[1], fontsize=12)
    axs[0, 0].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')
    axs[0, 0].set_xscale('log')
    axs[0, 0].set_ylabel('Probability', fontsize=12)
    # axs[0, 0].set_xlabel('Num. shots', fontsize=12)
    axs[0, 0].set_title('p-value')
    axs[0, 0].tick_params(direction="in")
    axs[0, 0].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[0, 1].plot(num_shots, fid_noiseless[:, 2], style[0], color=col[0])
    axs[0, 1].text(num_shots[-2], fid_noiseless[:, 2][-1] - 0.1, title[0], color=col[0], fontsize=12)
    axs[0, 1].plot(num_shots, fid_noiseless[:, 3], style[1], color=col[1])
    axs[0, 1].text(num_shots[-2], fid_noiseless[:, 3][-1] + 0.05, title[1], color=col[1], fontsize=12)
    axs[0, 1].set_xscale('log')
    # axs[0, 1].set_ylabel('Probability', fontsize=12)
    # axs[0, 0].set_xlabel('Num. shots', fontsize=12)
    axs[0, 1].set_title(r'Fidelity  $F(\rho_{B_n}, \rho_{expected})$')
    axs[0, 1].tick_params(direction="in")
    axs[0, 1].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[0, 2].plot(num_shots, fid_noiseless[:, 4], style[0], color=col[0])
    axs[0, 2].text(num_shots[-2], fid_noiseless[:, 4][-1] - 0.1, title[0], color=col[0], fontsize=12)
    axs[0, 2].plot(num_shots, fid_noiseless[:, 5], style[1], color=col[1])
    axs[0, 2].text(num_shots[-2], fid_noiseless[:, 5][-1] + 0.05, title[1], color=col[1], fontsize=12)
    axs[0, 2].set_xscale('log')
    # axs[0, 1].set_ylabel('Probability', fontsize=12)
    # axs[0, 0].set_xlabel('Num. shots', fontsize=12)
    axs[0, 2].set_title(r'Fidelity  $F(C_{B_n}, C_{expected})$')
    axs[0, 2].tick_params(direction="in")
    axs[0, 2].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[1, 0].plot(num_shots, fid_noisy[:, 0], style[0], color=col[0])
    axs[1, 0].text(num_shots[-2], fid_noisy[:, 0][-1] - 0.1, title[0], color=col[0], fontsize=12)
    axs[1, 0].plot(num_shots, fid_noisy[:, 1], style[1], color=col[1])
    axs[1, 0].text(num_shots[-2], fid_noisy[:, 1][-1] + 0.05, title[1], color=col[1], fontsize=12)
    axs[1, 0].set_xscale('log')
    axs[1, 0].set_ylabel('Probability', fontsize=12)
    axs[1, 0].set_xlabel('Num. shots', fontsize=12)
    # axs[0, 0].set_title('p-value')
    axs[1, 0].tick_params(direction="in")
    axs[1, 0].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[1, 1].plot(num_shots, fid_noisy[:, 2], style[0], color=col[0])
    axs[1, 1].text(num_shots[-2], fid_noisy[:, 2][-1] - 0.1, title[0], color=col[0], fontsize=12)
    axs[1, 1].plot(num_shots, fid_noisy[:, 3], style[1], color=col[1])
    axs[1, 1].text(num_shots[-2], fid_noisy[:, 3][-1] + 0.05, title[1], color=col[1], fontsize=12)
    axs[1, 1].set_xscale('log')
    # axs[0, 0].set_ylabel('Probability', fontsize=12)
    axs[1, 1].set_xlabel('Num. shots', fontsize=12)
    # axs[0, 0].set_title('p-value')
    axs[1, 1].tick_params(direction="in")
    axs[1, 1].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    axs[1, 2].plot(num_shots, fid_noisy[:, 4], style[0], color=col[0])
    axs[1, 2].text(num_shots[-2], fid_noisy[:, 4][-1] - 0.1, title[0], color=col[0], fontsize=12)
    axs[1, 2].plot(num_shots, fid_noisy[:, 5], style[1], color=col[1])
    axs[1, 2].text(num_shots[-2], fid_noisy[:, 5][-1] + 0.05, title[1], color=col[1], fontsize=12)
    axs[1, 2].set_xscale('log')
    # axs[1, 2].set_ylabel('Probability', fontsize=12)
    axs[1, 2].set_xlabel('Num. shots', fontsize=12)
    # axs[0, 0].set_title('p-value')
    axs[1, 2].tick_params(direction="in")
    axs[1, 2].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')

    plt.tight_layout()
    plt.show()
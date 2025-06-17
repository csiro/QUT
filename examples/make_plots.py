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
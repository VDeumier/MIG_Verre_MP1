# Generic imports
import math
from sklearn import metrics
import matplotlib.pyplot as plt

# Custom imports
from hummingbird.app.base_app        import *
from hummingbird.src.dataset.dataset import *
from hummingbird.src.agent.nn        import *

###############################################
### NN prediction on glass dataset
class nn_glass_mig_density_v2(base_app):
    def __init__(self):

        # Main parameters
        self.name = "nn_glass_mig_density_v2"

        # Initialize mother class
        super().__init__(self.name)

    def run(self):

        # Load dataset
        dts = dataset(pms(name="glass_mig_density_v2",
                          path="C:/Users/adelie.saule/MIG/hummingbird-master/hummingbird-master/hummingbird/dts/glass_mig_density_v2",
                          data=pms(type="array",
                                   filename="CompoD23.csv",     
                                   skiprows=1),
                          labels=pms(type="array",
                                     filename="D_2.2_3.csv",       
                                     skiprows=1)
                          )
                      )
        dts.load()

        # Normalize
        dts.normalize_data()

        # Split
        dts.split(0.1, 0.1, random=True)

        # Load nn
        net = nn(pms(model=pms(inp_dim=dts.n_features(),
                               arch=[500,500,100,50,1],
                               acts=["relu","relu","relu","relu","linear"]),
                     loss="mse",
                     lr=1.0e-4))

        # Convert dataset to torch tensors
        dts.to_torch()

        # Train
        loss = net.train(dts, 5000, 0.5)

        # Plot
        filename = "C:/Users/adelie.saule/MIG/hummingbird-master/hummingbird-master/results/nn_glass_mig/loss.png"
        plot_training(filename, loss[:,0], loss[:,1], loss[:,2], log_y=True)

        # Apply to test set
        xt, yt = dts.test_data()
        yp = net.apply(xt)
    
        
        # SiO2 Na2O Al2O3 B2O3 CaO MgO K2O Li2O PbO BaO ZnO
        # entree_manuelle = [73, 15, 1, 0, 7, 4, 0, 0, 0, 0, 0]   #verre microscope
        # mean = np.mean(entree_manuelle)
        # std = np.std(entree_manuelle)
        # entree_manuelle = (entree_manuelle - mean)/std
        # entree_manuelle = torch.Tensor(entree_manuelle)
        
        # sortie_manuelle = net.apply(entree_manuelle)
        
        # print("Densité verre microscope :", sortie_manuelle)
        # Plot predicted density again label
        filename = "C:/Users/adelie.saule/MIG/hummingbird-master/hummingbird-master/results/nn_glass_mig/comparison.png"
        y = np.hstack((yt, yp))
        e = np.abs(yt-yp)
        r_sqr = metrics.r2_score(yt, yp)
        plot_scatter(filename, y,
                     title="True density against prediction (test set), R² = " + str(round(r_sqr, 3)), c=e)
        print("# Average error on test set: "+str(np.mean(e.numpy())))
        
        # Save network parameters
        
        #net.dump("C:/Users/adelie.saule/MIG/Courbe_évolution_densité_SiO2_Na2O/net_density.txt")
        
        # Plot density SiO2-Na2O
        
        X = np.linspace(0, 50, 100)
        X_net = np.array([[100 - x, x, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for x in X])
        mean = np.mean(X_net, axis=0)       # On normalise les entrées
        std = np.std(X_net, axis=0)
        X_net = (X_net - mean)/std
        X_net[np.isnan(X_net)] = 0          # Remplace les 0/0 = NaN par des 0
        X_net = torch.Tensor(X_net)
        Y = list(net.apply(X_net))
        
        plt.clf()
        plt.plot(X, Y)
        plt.grid()
        plt.title("Composition: 100-x% SiO2, x% Na2O")
        plt.ylabel("Densité en g/cm3")
        plt.xlabel("x")
        plt.show()
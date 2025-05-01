import math

def predict(x):
    votes = [0, 0, 0, 0]
    if x[11] <= 127387.87109375:
        if x[0] <= 147.23077392578125:
            if x[8] <= 206.15384674072266:
                if x[8] <= -239.3653793334961:
                    if x[3] <= -479.9600067138672:
                        votes[0] += 1

                    else:
                        votes[0] += 1

                else:
                    if x[3] <= -979.6800231933594:
                        votes[0] += 1

                    else:
                        votes[3] += 1

            else:
                if x[6] <= -1489.5192260742188:
                    if x[11] <= 111638.0703125:
                        votes[2] += 1

                    else:
                        votes[0] += 1

                else:
                    if x[4] <= -5039.320068359375:
                        votes[1] += 1

                    else:
                        votes[0] += 1

        else:
            if x[2] <= 985.1922912597656:
                if x[1] <= 7.730769157409668:
                    votes[0] += 1

                else:
                    if x[7] <= 545.4999847412109:
                        votes[2] += 1

                    else:
                        votes[0] += 1

            else:
                votes[1] += 1

    else:
        if x[9] <= 6000.532470703125:
            votes[0] += 1

        else:
            if x[5] <= -8990.7998046875:
                votes[0] += 1

            else:
                votes[1] += 1

    # tree #2
    if x[11] <= 126904.8515625:
        if x[8] <= 207.94231414794922:
            if x[2] <= -31.557692527770996:
                if x[8] <= -596.2692260742188:
                    votes[0] += 1

                else:
                    if x[8] <= 202.53846740722656:
                        votes[3] += 1

                    else:
                        votes[0] += 1

            else:
                if x[9] <= 3541.368896484375:
                    votes[0] += 1

                else:
                    if x[9] <= 6079.741943359375:
                        votes[2] += 1

                    else:
                        votes[1] += 1

        else:
            if x[10] <= 4074.7772216796875:
                if x[12] <= 828.0:
                    votes[2] += 1

                else:
                    if x[7] <= 516.826904296875:
                        votes[2] += 1

                    else:
                        votes[0] += 1

            else:
                if x[10] <= 14165.54638671875:
                    if x[7] <= 1369.4422912597656:
                        votes[2] += 1

                    else:
                        votes[0] += 1

                else:
                    if x[2] <= 657.3461380004883:
                        votes[3] += 1

                    else:
                        votes[1] += 1

    else:
        if x[7] <= 566.0769348144531:
            votes[1] += 1

        else:
            if x[12] <= 4956.5:
                votes[0] += 1

            else:
                if x[7] <= 1285.0769653320312:
                    votes[1] += 1

                else:
                    votes[0] += 1

    # tree #3
    if x[8] <= 161.84615325927734:
        if x[10] <= 4319.7119140625:
            if x[7] <= -283.84616470336914:
                votes[3] += 1

            else:
                votes[0] += 1

        else:
            if x[7] <= -301.03846740722656:
                if x[9] <= 5820.18115234375:
                    votes[3] += 1

                else:
                    votes[1] += 1

            else:
                if x[5] <= 5325.3199462890625:
                    if x[0] <= 114.40384674072266:
                        votes[3] += 1

                    else:
                        votes[2] += 1

                else:
                    votes[1] += 1

    else:
        if x[10] <= 12602.27392578125:
            if x[7] <= 964.4230651855469:
                if x[1] <= -517.4615325927734:
                    votes[0] += 1

                else:
                    if x[2] <= 332.32122802734375:
                        votes[2] += 1

                    else:
                        votes[0] += 1

            else:
                votes[0] += 1

        else:
            if x[11] <= 57050.3125:
                votes[3] += 1

            else:
                votes[1] += 1

    # tree #4
    if x[7] <= 991.5192260742188:
        if x[10] <= 7729.521728515625:
            if x[10] <= 3427.5054931640625:
                if x[11] <= 20214.8916015625:
                    votes[2] += 1

                else:
                    if x[11] <= 30069.1728515625:
                        votes[0] += 1

                    else:
                        votes[0] += 1

            else:
                if x[10] <= 4973.56103515625:
                    if x[12] <= 2646.5:
                        votes[2] += 1

                    else:
                        votes[3] += 1

                else:
                    votes[2] += 1

        else:
            if x[6] <= -1213.3845825195312:
                if x[11] <= 154576.6875:
                    if x[9] <= 5839.49267578125:
                        votes[3] += 1

                    else:
                        votes[1] += 1

                else:
                    votes[1] += 1

            else:
                if x[11] <= 71584.125:
                    votes[3] += 1

                else:
                    votes[1] += 1

    else:
        if x[2] <= -281.01922607421875:
            if x[5] <= -1967.6799926757812:
                if x[3] <= 1642.1600341796875:
                    votes[3] += 1

                else:
                    votes[0] += 1

            else:
                votes[0] += 1

        else:
            if x[10] <= 16363.309326171875:
                votes[0] += 1

            else:
                votes[1] += 1

    # tree #5
    if x[12] <= 5148.0:
        if x[6] <= -1542.09619140625:
            if x[7] <= 328.3653869628906:
                if x[8] <= 133.7115364074707:
                    if x[5] <= 70.72000122070312:
                        votes[2] += 1

                    else:
                        votes[3] += 1

                else:
                    if x[6] <= -2038.4230346679688:
                        votes[2] += 1

                    else:
                        votes[2] += 1

            else:
                if x[10] <= 9492.18359375:
                    if x[6] <= -1877.40380859375:
                        votes[2] += 1

                    else:
                        votes[0] += 1

                else:
                    votes[3] += 1

        else:
            if x[10] <= 5170.685791015625:
                votes[0] += 1

            else:
                if x[6] <= -817.7307739257812:
                    if x[3] <= 1180.3999633789062:
                        votes[3] += 1

                    else:
                        votes[2] += 1

                else:
                    votes[1] += 1

    else:
        if x[10] <= 7335.6875:
            if x[12] <= 6453.5:
                votes[3] += 1

            else:
                votes[0] += 1

        else:
            if x[9] <= 5901.9833984375:
                votes[3] += 1

            else:
                votes[1] += 1

    # tree #6
    if x[2] <= 589.8461608886719:
        if x[8] <= 177.9423065185547:
            if x[10] <= 4319.7119140625:
                if x[7] <= -296.9038429260254:
                    votes[3] += 1

                else:
                    votes[0] += 1

            else:
                if x[9] <= 6405.352294921875:
                    if x[12] <= 2856.0:
                        votes[3] += 1

                    else:
                        votes[3] += 1

                else:
                    votes[1] += 1

        else:
            if x[7] <= 948.9999694824219:
                if x[2] <= 359.0327606201172:
                    if x[12] <= 4744.5:
                        votes[2] += 1

                    else:
                        votes[1] += 1

                else:
                    votes[0] += 1

            else:
                votes[0] += 1

    else:
        if x[9] <= 4648.9517822265625:
            votes[0] += 1

        else:
            votes[1] += 1

    # tree #7
    if x[7] <= 991.5192260742188:
        if x[4] <= 1805.9600219726562:
            if x[4] <= -2125.760009765625:
                if x[1] <= -375.4423179626465:
                    votes[1] += 1

                else:
                    if x[12] <= 4266.5:
                        votes[0] += 1

                    else:
                        votes[1] += 1

            else:
                if x[8] <= 161.84615325927734:
                    if x[10] <= 3632.5399169921875:
                        votes[0] += 1

                    else:
                        votes[3] += 1

                else:
                    if x[12] <= 4881.0:
                        votes[2] += 1

                    else:
                        votes[1] += 1

        else:
            if x[10] <= 5199.8646240234375:
                votes[0] += 1

            else:
                votes[1] += 1

    else:
        if x[6] <= -1750.7114868164062:
            if x[7] <= 1080.3077087402344:
                votes[0] += 1

            else:
                if x[3] <= -1412.3199462890625:
                    votes[1] += 1

                else:
                    votes[3] += 1

        else:
            if x[12] <= 3112.0:
                votes[0] += 1

            else:
                if x[3] <= 429.0:
                    votes[0] += 1

                else:
                    if x[6] <= 49.519287109375:
                        votes[3] += 1

                    else:
                        votes[0] += 1

    # tree #8
    if x[1] <= 594.5576782226562:
        if x[7] <= 1014.3461303710938:
            if x[11] <= 126904.8515625:
                if x[0] <= 200.34615325927734:
                    if x[5] <= 195.0:
                        votes[2] += 1

                    else:
                        votes[3] += 1

                else:
                    votes[0] += 1

            else:
                if x[3] <= -2367.0399169921875:
                    if x[9] <= 7165.477294921875:
                        votes[0] += 1

                    else:
                        votes[1] += 1

                else:
                    if x[10] <= 6178.5863037109375:
                        votes[0] += 1

                    else:
                        votes[1] += 1

        else:
            if x[1] <= -97.15384674072266:
                votes[0] += 1

            else:
                if x[10] <= 12685.376708984375:
                    votes[0] += 1

                else:
                    votes[3] += 1

    else:
        if x[9] <= 5035.8453369140625:
            votes[0] += 1

        else:
            votes[1] += 1

    # tree #9
    if x[7] <= 325.26922607421875:
        if x[12] <= 5216.0:
            if x[8] <= 163.40384674072266:
                if x[2] <= 151.0384635925293:
                    votes[3] += 1

                else:
                    if x[6] <= -1924.7115478515625:
                        votes[0] += 1

                    else:
                        votes[1] += 1

            else:
                if x[12] <= 4520.0:
                    if x[6] <= -841.1523208618164:
                        votes[2] += 1

                    else:
                        votes[0] += 1

                else:
                    votes[1] += 1

        else:
            if x[12] <= 5603.5:
                if x[9] <= 6225.792236328125:
                    votes[3] += 1

                else:
                    votes[1] += 1

            else:
                votes[1] += 1

    else:
        if x[10] <= 9234.59326171875:
            if x[10] <= 4001.800048828125:
                if x[3] <= 1453.9199829101562:
                    if x[7] <= 364.5:
                        votes[0] += 1

                    else:
                        votes[0] += 1

                else:
                    if x[3] <= 1687.9199829101562:
                        votes[2] += 1

                    else:
                        votes[0] += 1

            else:
                if x[12] <= 3406.0:
                    if x[6] <= -1727.3461303710938:
                        votes[2] += 1

                    else:
                        votes[3] += 1

                else:
                    votes[0] += 1

        else:
            if x[5] <= 3886.4798583984375:
                votes[3] += 1

            else:
                votes[1] += 1

    # tree #10
    if x[9] <= 6173.097900390625:
        if x[2] <= -47.82692337036133:
            if x[1] <= -295.4038391113281:
                votes[0] += 1

            else:
                if x[10] <= 9759.226806640625:
                    if x[8] <= 50.51922941207886:
                        votes[0] += 1

                    else:
                        votes[2] += 1

                else:
                    votes[3] += 1

        else:
            if x[7] <= 373.51922607421875:
                if x[2] <= -2.9615384340286255:
                    if x[9] <= 4777.6527099609375:
                        votes[2] += 1

                    else:
                        votes[3] += 1

                else:
                    if x[6] <= -1788.6345825195312:
                        votes[2] += 1

                    else:
                        votes[2] += 1

            else:
                if x[10] <= 4074.7772216796875:
                    if x[8] <= 246.21153259277344:
                        votes[0] += 1

                    else:
                        votes[0] += 1

                else:
                    if x[6] <= -1575.75:
                        votes[2] += 1

                    else:
                        votes[0] += 1

    else:
        if x[7] <= 655.6923065185547:
            votes[1] += 1

        else:
            if x[4] <= -1992.1200256347656:
                votes[0] += 1

            else:
                votes[1] += 1

    # return argmax of votes
    classIdx = 0
    maxVotes = votes[0]

    for i in range(1, 4):
        if votes[i] > maxVotes:
            classIdx = i
            maxVotes = votes[i]

    return int(classIdx)

#                    *
#                    * Predict readable class name
#                    
def predictLabel(x):
    return idxToLabel(predict(x))

#                    *
#                    * Convert class idx to readable name
#                    
def idxToLabel(classIdx):
    if classIdx == 0:
        return "Normal"
    if classIdx == 1:
        return "Crash"
    if classIdx == 2:
        return "Braking"
    if classIdx == 3:
        return "Falling"
    return "Houston we have a problem"

def vector_magnitudes(data):
    return [math.sqrt(x**2 + y**2 + z**2) for x, y, z in data]

def mean(data):
    return sum(data) / len(data) if data else 0

def max_abs(data):
    return max(abs(x) for x in data)

def calculate_kinematic_features(second_data):
    accel_samples = []
    gyro_samples = []

    i = 0
    while i < len(second_data):
        tag = second_data[i]
        if tag == 1:
            # Accelerometer sample
            accel_samples.append([
                second_data[i+1],  # accel_x
                second_data[i+2],  # accel_y
                second_data[i+3],  # accel_z
            ])
        elif tag == 2:
            # Gyroscope sample
            gyro_samples.append([
                second_data[i+1],  # gyro_x
                second_data[i+2],  # gyro_y
                second_data[i+3],  # gyro_z
            ])
        # Move to next group (4 values: tag + 3 axes)
        i += 4

    # Fallback to a dummy row if no samples are available
    accel = accel_samples if accel_samples else [[0, 0, 0]]
    gyro = gyro_samples if gyro_samples else [[0, 0, 0]]

    # Compute jerk as difference between consecutive accel samples, scaled by 26
    jerk = []

    if len(accel) >= 2:
        for i in range(1, len(accel)):
            dx = (accel[i][0] - accel[i-1][0]) * 26
            dy = (accel[i][1] - accel[i-1][1]) * 26
            dz = (accel[i][2] - accel[i-1][2]) * 26
            jerk.append([dx, dy, dz])
    else:
        jerk = [[0, 0, 0]]


    # Magnitudes
    accel_magnitude = vector_magnitudes(accel)
    gyro_magnitude = vector_magnitudes(gyro)
    jerk_magnitude = vector_magnitudes(jerk)

    # Extract components
    accel_x = [v[0] for v in accel]
    accel_y = [v[1] for v in accel]
    accel_z = [v[2] for v in accel]

    jerk_x = [v[0] for v in jerk]
    jerk_y = [v[1] for v in jerk]
    jerk_z = [v[2] for v in jerk]

    gyro_x = [v[0] for v in gyro]
    gyro_y = [v[1] for v in gyro]
    gyro_z = [v[2] for v in gyro]

    features = {
        'accel_x_mean': mean(accel_x),
        'accel_y_mean': mean(accel_y),
        'accel_z_mean': mean(accel_z),
        'jerk_x_mean': mean(jerk_x),
        'jerk_y_mean': mean(jerk_y),
        'jerk_z_mean': mean(jerk_z),
        'gyro_x_mean': mean(gyro_x),
        'gyro_y_mean': mean(gyro_y),
        'gyro_z_mean': mean(gyro_z),
        'accel_peak': max(accel_magnitude),
        'gyro_peak': max(gyro_magnitude),
        'jerk_peak': max(jerk_magnitude),
        'accel_z_peak': max_abs(accel_z),
    }
    return features

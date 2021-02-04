def truncate(string):
    MAX = 250
    truncated = ''
    punctuation ='.?!'
    for l in string:
        truncated += l
        if len(truncated) > MAX and l in punctuation:
            break
    return truncated

desc = 'One month after her novel Gone With the Wind was published, Margaret Mitchell sold the movie rights for fifty thousand dollars. Fearful of what the studio might do to her story—“I wouldn’t put it beyond Hollywood to have . . . Scarlett seduce General Sherman,” she joked—the author washed her hands of involvement with the film. However, driven by a maternal interest in her literary firstborn and compelled by her Southern manners to answer every fan letter she received, Mitchell was unable to stay aloof for long. In this collection of her letters about the 1939 motion picture classic, readers have a front-row seat as the author watches the Dream Factory at work, learning the ins and outs of filmmaking and discovering the peculiarities of a movie-crazed public. Her ability to weave a story, so evident in Gone With the Wind, makes for delightful reading in her correspondence with a who’s who of Hollywood, from producer David O. Selznick, director George Cukor, and screenwriter Sidney Howard, to cast members Clark Gable, Vivien Leigh, Leslie Howard, Olivia de Havilland and Hattie McDaniel. Mitchell also wrote to thousands of '


print(truncate(desc))
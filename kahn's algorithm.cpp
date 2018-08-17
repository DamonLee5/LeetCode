class Solution {
public:
    bool canFinish(int numCourses, vector<pair<int, int>>& prerequisites) {
        unordered_set<int> result;
        unordered_set<int> next;
        int a[numCourses]={0};
        bool b[numCourses][numCourses];
        memset(b,0,sizeof(b));
        int pl=prerequisites.size();
        for (int i=0;i<pl;i++)
        {
            a[prerequisites[i].first]++;
            b[prerequisites[i].first][prerequisites[i].second]=1;
        }
        for (int i=0;i<numCourses;i++)
        {
            if(a[i]==0)
                next.insert(i);
        }
        unordered_set<int>::iterator it;
        while (!next.empty())
        {
            it=next.begin();
            int nn=(*it);
            result.insert(nn);
            next.erase(it);
            for (int i=0;i<numCourses;i++)
                if(b[i][nn])
                {
                    b[i][nn]=false;
                    pl--;
                    a[i]--;
                    if(a[i]==0) next.insert(i);
                }
        }
        if(pl==0) return true;
        else return false;
    }
};
//Next challenges: Alien Dictionary// Minimum Height Trees// Sequence Reconstruction// Course Schedule III
